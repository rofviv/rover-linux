#include <Arduino.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>
#include <freertos/semphr.h>

/* =====================  PINES  ===================== */
// PWM recomendados en ESP32 (puedes cambiar mientras sean GPIO válidos)
#define THR_A_PIN      4   // PWM A
#define THR_B_PIN      16  // PWM B
#define REVERSA1_PIN   18  // Dirección/Reversa 1
#define REVERSA2_PIN   19  // Dirección/Reversa 2

/* =====================  PWM / RAMPAS / TIEMPOS  ===================== */
// Interfaz de comandos mantiene 0..255 como en tu sketch
const uint8_t  PWM_MIN_8B      = 0;
const uint8_t  PWM_MAX_8B      = 255;

// LEDC (PWM de ESP32)
const int      LEDC_CH_A       = 0;
const int      LEDC_CH_B       = 1;
const int      LEDC_RES_BITS   = 10;         // 10 bits -> 0..1023
const int      LEDC_MAX_10B    = (1 << LEDC_RES_BITS) - 1;
const uint32_t LEDC_FREQ_HZ    = 20000;      // 20 kHz para motores/puentes

// Rampa equivalente a tu RAMP_MS original (ms por paso de 1/255)
const uint16_t RAMP_MS_PER_STEP = 4;         // ms/step @ escala 0..255

// Tarea de control periódica
const uint32_t CTRL_DT_MS       = 5;         // periodo de control (no bloquea)

/* =====================  RTOS HANDLES  ===================== */
TaskHandle_t   hTaskSerial = nullptr;
TaskHandle_t   hTaskCtrl   = nullptr;
QueueHandle_t  qCmd        = nullptr;

/* =====================  COMANDOS  ===================== */
enum CmdType : uint8_t {
  CMD_SET_A,      // payload: value 0..255
  CMD_SET_B,      // payload: value 0..255
  CMD_SET_D,      // NUEVO: aplica el mismo PWM a ambos motores
  CMD_STOP_BOTH,  // sin payload
  CMD_REV_0,      // ambas reversas LOW
  CMD_REV_1,      // pedir reversa1
  CMD_REV_2       // pedir reversa2
};

struct Command {
  CmdType type;
  uint16_t value; // usado en SET_A/SET_B/SET_D
};

/* =====================  ESTADO DEL CONTROL  ===================== */
static float   currA_8b = 0.0f,   currB_8b = 0.0f;      // PWM actual (0..255)
static float   tgtA_8b  = 0.0f,   tgtB_8b  = 0.0f;      // PWM objetivo (0..255)

// Dirección solicitada y aplicada
enum RevState : uint8_t { REV_NONE=0, REV_1, REV_2 };
static RevState desiredRev = REV_NONE;
static RevState activeRev  = REV_NONE;

// Velocidad de rampa (steps de 8 bits por ms)
static const float ramp_steps_per_ms = 1.0f / (float)RAMP_MS_PER_STEP;
// Tolerancia para considerar “cero” (por ruido/quantización)
static const float EPS_ZERO = 1.0f;

/* =====================  UTILIDADES  ===================== */
// Mapea 0..255 a 0..1023 (10 bits LEDC)
static inline uint32_t map8b_to_10b(float v8) {
  if (v8 < 0) v8 = 0;
  if (v8 > 255) v8 = 255;
  // redondeo
  return (uint32_t)lroundf((v8 / 255.0f) * (float)LEDC_MAX_10B);
}

static inline void applyPWM_LEDC() {
  ledcWrite(LEDC_CH_A, map8b_to_10b(currA_8b));
  ledcWrite(LEDC_CH_B, map8b_to_10b(currB_8b));
}

static inline bool bothAtZero() {
  return (fabsf(currA_8b) <= EPS_ZERO) && (fabsf(currB_8b) <= EPS_ZERO)
         && (fabsf(tgtA_8b) <= EPS_ZERO) && (fabsf(tgtB_8b) <= EPS_ZERO);
}

static inline void setReversePins(RevState r) {
  switch (r) {
    case REV_NONE:
      digitalWrite(REVERSA1_PIN, LOW);
      digitalWrite(REVERSA2_PIN, LOW);
      break;
    case REV_1:
      digitalWrite(REVERSA1_PIN, HIGH);
      digitalWrite(REVERSA2_PIN, LOW);
      break;
    case REV_2:
      digitalWrite(REVERSA1_PIN, LOW);
      digitalWrite(REVERSA2_PIN, HIGH);
      break;
  }
}

/* =====================  TAREA: CONTROL (core 1)  ===================== */
void taskControl(void *pv) {
  TickType_t t0 = xTaskGetTickCount();

  for (;;) {
    // --- 1) Consume todos los comandos pendientes sin bloquear
    Command cmd;
    while (xQueueReceive(qCmd, &cmd, 0) == pdTRUE) {
      switch (cmd.type) {
        case CMD_SET_A:
          tgtA_8b = constrain((int)cmd.value, PWM_MIN_8B, PWM_MAX_8B);
          break;
        case CMD_SET_B:
          tgtB_8b = constrain((int)cmd.value, PWM_MIN_8B, PWM_MAX_8B);
          break;
        case CMD_SET_D:   // NUEVO comando
          tgtA_8b = constrain((int)cmd.value, PWM_MIN_8B, PWM_MAX_8B);
          tgtB_8b = constrain((int)cmd.value, PWM_MIN_8B, PWM_MAX_8B);
          break;
        case CMD_STOP_BOTH:
          tgtA_8b = 0.0f;
          tgtB_8b = 0.0f;
          break;
        case CMD_REV_0:
          desiredRev = REV_NONE;
          setReversePins(REV_NONE);
          activeRev = REV_NONE;
          break;
        case CMD_REV_1:
          desiredRev = REV_1;
          tgtA_8b = 0.0f;
          tgtB_8b = 0.0f;
          break;
        case CMD_REV_2:
          desiredRev = REV_2;
          tgtA_8b = 0.0f;
          tgtB_8b = 0.0f;
          break;
      }
    }

    // --- 2) Rampa no bloqueante hacia los objetivos (A y B)
    const float dt_ms = (float)CTRL_DT_MS;
    const float step  = ramp_steps_per_ms * dt_ms;  // pasos de 8 bits en este ciclo

    auto rampTo = [&](float curr, float tgt) -> float {
      if (fabsf(tgt - curr) <= step) return tgt;            // alcanzado
      return (tgt > curr) ? (curr + step) : (curr - step);  // avanza
    };

    currA_8b = rampTo(currA_8b, tgtA_8b);
    currB_8b = rampTo(currB_8b, tgtB_8b);

    // --- 3) Si se solicitó reversa y ambos canales llegaron a 0, aplicar cambio
    if (desiredRev != activeRev && bothAtZero()) {
      setReversePins(desiredRev);
      activeRev = desiredRev;
    }

    // --- 4) Aplicar PWM a hardware
    applyPWM_LEDC();

    // --- 5) Telemetría ocasional (no saturar Serial)
    static uint32_t cnt = 0;
    if ((cnt++ % (1000 / CTRL_DT_MS)) == 0) { // ~1 Hz
      Serial.printf("A=%.0f  B=%.0f  R1=%d  R2=%d\n",
                    currA_8b, currB_8b,
                    digitalRead(REVERSA1_PIN),
                    digitalRead(REVERSA2_PIN));
    }

    // --- 6) Temporización exacta
    vTaskDelayUntil(&t0, pdMS_TO_TICKS(CTRL_DT_MS));
  }
}

/* =====================  TAREA: SERIAL / PARSER (core 0)  ===================== */
void taskSerial(void *pv) {
  String linea;
  linea.reserve(32);

  for (;;) {
    while (Serial.available()) {
      char c = (char)Serial.read();

      if (c == '\n' || c == '\r') {
        if (linea.length() == 0) continue;
        linea.trim();

        Command cmd{};
        bool recognized = true;

        if (linea == "0") {
          cmd.type = CMD_STOP_BOTH;

        } else if (linea.equalsIgnoreCase("R1")) {
          cmd.type = CMD_REV_1;

        } else if (linea.equalsIgnoreCase("R2")) {
          cmd.type = CMD_REV_2;

        } else if (linea.equalsIgnoreCase("R0")) {
          cmd.type = CMD_REV_0;

        } else if (linea[0] == 'A' || linea[0] == 'a') {
          int val = linea.substring(1).toInt();
          val = constrain(val, PWM_MIN_8B, PWM_MAX_8B);
          cmd.type  = CMD_SET_A;
          cmd.value = (uint16_t)val;

        } else if (linea[0] == 'B' || linea[0] == 'b') {
          int val = linea.substring(1).toInt();
          val = constrain(val, PWM_MIN_8B, PWM_MAX_8B);
          cmd.type  = CMD_SET_B;
          cmd.value = (uint16_t)val;

        } else if (linea[0] == 'D' || linea[0] == 'd') {   // NUEVO
          int val = linea.substring(1).toInt();
          val = constrain(val, PWM_MIN_8B, PWM_MAX_8B);
          cmd.type  = CMD_SET_D;
          cmd.value = (uint16_t)val;

        } else {
          recognized = false;
          Serial.println(F("Comando invalido"));
        }

        if (recognized) {
          xQueueSend(qCmd, &cmd, 0);
        }
        linea = "";

      } else {
        linea += c;
        if (linea.length() > 24) linea = "";  // protección simple
      }
    }
    vTaskDelay(pdMS_TO_TICKS(2)); // cede CPU; evita busy-wait
  }
}

/* =====================  SETUP / LOOP  ===================== */
void setup() {
  // Serial
  Serial.begin(115200);
  delay(100);
  Serial.println(F(
    "Comandos:\n"
    "A### o B### (0-255) para fijar PWM individual.\n"
    "D### aplica el mismo PWM a ambos motores.\n"
    "R1 activa Reversa1 | R2 activa Reversa2 | R0 apaga ambas.\n"
    "0 detiene ambos con rampa.\n"
    "Ej.: A200  |  B120  |  D180  | 0"
  ));

  // Pines
  pinMode(REVERSA1_PIN, OUTPUT);
  pinMode(REVERSA2_PIN, OUTPUT);
  setReversePins(REV_NONE);

  // LEDC PWM
  ledcSetup(LEDC_CH_A, LEDC_FREQ_HZ, LEDC_RES_BITS);
  ledcSetup(LEDC_CH_B, LEDC_FREQ_HZ, LEDC_RES_BITS);
  ledcAttachPin(THR_A_PIN, LEDC_CH_A);
  ledcAttachPin(THR_B_PIN, LEDC_CH_B);
  ledcWrite(LEDC_CH_A, 0);
  ledcWrite(LEDC_CH_B, 0);

  // RTOS queue
  qCmd = xQueueCreate(10, sizeof(Command));

  // Crear tareas fijadas a núcleos
  xTaskCreatePinnedToCore(taskSerial, "SERIAL_PARSER", 4096, nullptr, 2, &hTaskSerial, 0); // core 0
  xTaskCreatePinnedToCore(taskControl, "CONTROL_LOOP", 4096, nullptr, 3, &hTaskCtrl,   1); // core 1
}

void loop() {
  // vacío: todo corre en tareas
}