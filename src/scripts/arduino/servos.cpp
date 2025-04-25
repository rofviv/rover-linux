#define THR_A_PIN 44
#define THR_B_PIN 45

const uint8_t PWM_MIN = 0;
const uint8_t PWM_MAX = 255;
const uint16_t RAMP_MS = 4;
const float FACTOR_COMPENSACION_B = 1.0;

uint8_t velA = 0, velB = 0;
String   linea = "";

void rampa(uint8_t &actual, uint8_t destino, uint8_t pin) {
  if (actual < destino) {
    while (actual < destino) {
      actual++;
      analogWrite(pin, actual);
      delay(RAMP_MS);
    }
  } else if (actual > destino) {
    while (actual > destino) {
      actual--;
      analogWrite(pin, actual);
      delay(RAMP_MS);
    }
  }
}

void rampaSincronizada(uint8_t &velActualA, uint8_t &velActualB, uint8_t velocidadDestino) {
  while (velActualA != velocidadDestino || velActualB != velocidadDestino) {
    if (velActualA < velocidadDestino) {
      velActualA++;
      analogWrite(THR_A_PIN, velActualA);
    } else if (velActualA > velocidadDestino) {
      velActualA--;
      analogWrite(THR_A_PIN, velActualA);
    }
    
    if (velActualB < velocidadDestino) {
      velActualB++;
      analogWrite(THR_B_PIN, velActualB * FACTOR_COMPENSACION_B);
    } else if (velActualB > velocidadDestino) {
      velActualB--;
      analogWrite(THR_B_PIN, velActualB * FACTOR_COMPENSACION_B);
    }
    
    delay(RAMP_MS);
  }
}

void moverAmbos(uint8_t velocidad) {
  velocidad = constrain(velocidad, PWM_MIN, PWM_MAX);
  rampaSincronizada(velA, velB, velocidad);
}

void setup() {
  pinMode(THR_A_PIN, OUTPUT);
  pinMode(THR_B_PIN, OUTPUT);
  analogWrite(THR_A_PIN, 0);
  analogWrite(THR_B_PIN, 0);
  Serial.begin(9600);
  Serial.println("Control de motores:");
  Serial.println("A### - Controla motor A (0-255)");
  Serial.println("B### - Controla motor B (0-255)");
  Serial.println("M### - Controla ambos motores (0-255)");
  Serial.println("0 - Detiene ambos motores");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    
    if (c == '\n') {
      if (linea == "0") {
        moverAmbos(0);
        Serial.println("Motores detenidos");
      }
      else if (linea.startsWith("A0B")) {  // Giro izquierda
        String valor = linea.substring(3);
        int velocidad = valor.toInt();
        velocidad = constrain(velocidad, PWM_MIN, PWM_MAX);
        rampa(velA, 0, THR_A_PIN);
        rampa(velB, velocidad, THR_B_PIN);
        Serial.println("Girando izquierda");
      }
      else if (linea.startsWith("B0A")) {  // Giro derecha
        String valor = linea.substring(3);
        int velocidad = valor.toInt();
        velocidad = constrain(velocidad, PWM_MIN, PWM_MAX);
        rampa(velB, 0, THR_B_PIN);
        rampa(velA, velocidad, THR_A_PIN);
        Serial.println("Girando derecha");
      }
      else if (linea.startsWith("M")) {  // Ambos motores
        String valor = linea.substring(1);
        int velocidad = valor.toInt();
        moverAmbos(velocidad);
        Serial.print("Ambos motores a velocidad: ");
        Serial.println(velocidad);
      }
      
      Serial.print("Estado actual - A: ");
      Serial.print(velA);
      Serial.print(" B: ");
      Serial.println(velB);
      
      linea = "";
    }
    else if (linea.length() < 16) {
      linea += c;
    }
  }
}