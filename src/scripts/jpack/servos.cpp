#define THR_A_PIN 5
#define THR_B_PIN 6

const uint8_t PWM_MIN = 0;
const uint8_t PWM_MAX = 255;
const uint16_t RAMP_MS = 4;

// Factores de compensación iniciales
float factorCompensacionA = 1.0;
float factorCompensacionB = 1.0;

uint8_t velA = 0, velB = 0;
String linea = "";

void rampaParalela(uint8_t &actualA, uint8_t destinoA, uint8_t &actualB, uint8_t destinoB, float factorA, float factorB) {
  actualA = constrain(destinoA, PWM_MIN, PWM_MAX);
  actualB = constrain(destinoB, PWM_MIN, PWM_MAX);

  analogWrite(THR_A_PIN, constrain(actualA * factorA, 0, 255));
  analogWrite(THR_B_PIN, constrain(actualB * factorB, 0, 255));
}


void setup() {
  pinMode(THR_A_PIN, OUTPUT);
  pinMode(THR_B_PIN, OUTPUT);
  analogWrite(THR_A_PIN, 0);
  analogWrite(THR_B_PIN, 0);
  Serial.begin(9600);
  Serial.println("Control de motores con rampas sincronizadas:");
  Serial.println("Formato M<velA>-<factorA>,<velB>-<factorB>");
  Serial.println("Ejemplo: M100-1,100-1");
  Serial.println("0 para detener motores");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    
    if (c == '\n') {
      linea.trim();
      
      if (linea == "0") {
        rampaParalela(velA, 0, velB, 0, factorCompensacionA, factorCompensacionB);
        Serial.println("Motores detenidos");
      }
      else if (linea.startsWith("M")) {
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
      }
      
      Serial.print("Estado actual - A: ");
      Serial.print(velA);
      Serial.print(" (factor ");
      Serial.print(factorCompensacionA);
      Serial.print("), B: ");
      Serial.print(velB);
      Serial.print(" (factor ");
      Serial.print(factorCompensacionB);
      Serial.println(")");
      
      linea = "";
    }
    else if (linea.length() < 64) {
      linea += c;
    }
  }
}
