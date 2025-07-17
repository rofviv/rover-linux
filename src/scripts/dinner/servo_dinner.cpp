#define THR_A_PIN 44
#define THR_B_PIN 45
#define REVERSA1_PIN 46
#define REVERSA2_PIN 47

const uint8_t PWM_MIN = 0;
const uint8_t PWM_MAX = 255;
const uint16_t RAMP_MS = 4;

// Factores de compensación iniciales
float factorCompensacionA = 1.0;
float factorCompensacionB = 1.0;

uint8_t velA = 0, velB = 0;
String   linea = "";

void rampaParalela(uint8_t &actualA, uint8_t destinoA, uint8_t &actualB, uint8_t destinoB, float factorA, float factorB) {
  actualA = constrain(destinoA, PWM_MIN, PWM_MAX);
  actualB = constrain(destinoB, PWM_MIN, PWM_MAX);

  analogWrite(THR_A_PIN, constrain(actualA * factorA, 0, 255));
  analogWrite(THR_B_PIN, constrain(actualB * factorB, 0, 255));
}

void imprimir() {
  Serial.print(F("A=")); Serial.print(velA);
  Serial.print(F("  B=")); Serial.print(velB);
  Serial.print(F("  R1=")); Serial.print(digitalRead(REVERSA1_PIN));
  Serial.print(F("  R2=")); Serial.println(digitalRead(REVERSA2_PIN));
}

void setup() {
  pinMode(THR_A_PIN, OUTPUT);
  pinMode(THR_B_PIN, OUTPUT);
  pinMode(REVERSA1_PIN, OUTPUT);
  pinMode(REVERSA2_PIN, OUTPUT);

  analogWrite(THR_A_PIN, velA);
  analogWrite(THR_B_PIN, velB);
  digitalWrite(REVERSA1_PIN, LOW);
  digitalWrite(REVERSA2_PIN, LOW);

  Serial.begin(9600);
  Serial.println(F(
    "Comandos:\n"
    "A### o B### (0‑255) para fijar PWM.\n"
    "R1 activa Reversa1 | R2 activa Reversa2 | R0 apaga ambas.\n"
    "Ej.: A200  |  B120  | 0 para detener ambos"));
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n' || c == '\r') {
      if (linea.length() == 0) continue;
      linea.trim();

      if (linea == "0") {
        rampaParalela(velA, 0, velB, 0, factorCompensacionA, factorCompensacionB);
        Serial.println("Motores detenidos");
      } else if (linea == "R1 on" || linea == "r1 on") {
        digitalWrite(REVERSA1_PIN, HIGH);
      } else if (linea == "R1 off" || linea == "r1 off") {
        digitalWrite(REVERSA1_PIN, LOW);
      } else if (linea == "R2 on" || linea == "r2 on") {
        digitalWrite(REVERSA2_PIN, HIGH);
      } else if (linea == "R2 off" || linea == "r2 off") {
        digitalWrite(REVERSA2_PIN, LOW);
      } else if (linea == "RA on" || linea == "ra on") {
        digitalWrite(REVERSA1_PIN, HIGH);
        digitalWrite(REVERSA2_PIN, HIGH);
      } else if (linea == "RA off" || linea == "ra off") {
        digitalWrite(REVERSA1_PIN, LOW);
        digitalWrite(REVERSA2_PIN, LOW);
      } else if (linea.startsWith("M")) {
        int comaIndex = linea.indexOf(',');
        if (comaIndex > 1) {
          String parteA = linea.substring(1, comaIndex);
          String parteB = linea.substring(comaIndex + 1);

          int guionA = parteA.indexOf('-');
          int guionB = parteB.indexOf('-');

          if (guionA > 0 && guionB > 0) {
            String valorA = parteA.substring(0, guionA);
            String factorA = parteA.substring(guionA + 1);

            String valorB = parteB.substring(0, guionB);
            String factorB = parteB.substring(guionB + 1);

            int velocidadA = constrain(valorA.toInt(), PWM_MIN, PWM_MAX);
            int velocidadB = constrain(valorB.toInt(), PWM_MIN, PWM_MAX);

            factorCompensacionA = factorA.toFloat();
            factorCompensacionB = factorB.toFloat();

            Serial.print("Recibido -> A: ");
            Serial.print(velocidadA);
            Serial.print(" (factor ");
            Serial.print(factorCompensacionA);
            Serial.print("), B: ");
            Serial.print(velocidadB);
            Serial.print(" (factor ");
            Serial.print(factorCompensacionB);
            Serial.println(")");

            rampaParalela(velA, velocidadA, velB, velocidadB, factorCompensacionA, factorCompensacionB);
          } else {
            Serial.println("Formato incorrecto. Debe ser M<velA>-<factorA>,<velB>-<factorB>");
          }
        } else {
          Serial.println("Formato incorrecto en comando M");
        }
      } else {
        Serial.println(F("Comando invalido"));
      }
      imprimir();
      linea = "";
    } else {
      linea += c;
      if (linea.length() > 16) linea = "";
    }
  }
}