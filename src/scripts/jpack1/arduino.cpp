#define THR_A_PIN 44
#define THR_B_PIN 45
#define RELAY1_PIN 46
#define RELAY2_PIN 47

const uint8_t PWM_MIN = 0;
const uint8_t PWM_MAX = 255;
const uint16_t RAMP_MS = 4;

uint8_t velA = 0, velB = 0;
String   linea = "";

void rampa(uint8_t &actual, uint8_t destino, uint8_t pin) {
  if (actual == destino) return;
  int8_t dir = (destino > actual) ? 1 : -1;
  for (uint8_t v = actual; v != destino; v += dir) {
    analogWrite(pin, v);
    delay(RAMP_MS);
  }
  actual = destino;
}

void imprimir() {
  Serial.print(F("A=")); Serial.print(velA);
  Serial.print(F("  B=")); Serial.println(velB);
}

void setup() {
  pinMode(THR_A_PIN, OUTPUT);
  pinMode(THR_B_PIN, OUTPUT);
  analogWrite(THR_A_PIN, velA);
  analogWrite(THR_B_PIN, velB);

  // Configurar pines de relés
  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);
  digitalWrite(RELAY1_PIN, HIGH); // Relé apagado al inicio
  digitalWrite(RELAY2_PIN, HIGH); // Relé apagado al inicio

  Serial.begin(9600);
  Serial.println(F(
    "Comandos disponibles:\n"
    " A###   -> PWM en pin 44\n"
    " B###   -> PWM en pin 45\n"
    " M###   -> PWM en pin 44 y 45\n"
    " R1     -> Activa rele pin 46\n"
    " R1OFF  -> Desactiva rele pin 46\n"
    " R2     -> Activa rele pin 47\n"
    " R2OFF  -> Desactiva rele pin 47\n"
    " RALL   -> Activa todos los relés\n"
    " RALLOFF-> Desactiva todos los relés\n"
    " 0      -> Detiene ambos PWM"));
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n' || c == '\r') {          // fin de línea
      if (linea.length() == 0) continue;
      linea.trim();

      if (linea == "0") {
        rampa(velA, 0, THR_A_PIN);
        rampa(velB, 0, THR_B_PIN);
      } else if (linea[0] == 'M' || linea[0] == 'm') {
        int val = linea.substring(1).toInt();
        val = constrain(val, PWM_MIN, PWM_MAX);
        rampa(velA, val, THR_A_PIN);
        rampa(velB, val, THR_B_PIN);
      } else if (linea[0] == 'A' || linea[0] == 'a') {
        int val = linea.substring(1).toInt();
        val = constrain(val, PWM_MIN, PWM_MAX);
        rampa(velA, val, THR_A_PIN);
      } else if (linea[0] == 'B' || linea[0] == 'b') {
        int val = linea.substring(1).toInt();
        val = constrain(val, PWM_MIN, PWM_MAX);
        rampa(velB, val, THR_B_PIN);

      // Control de Relés
      } else if (linea.equalsIgnoreCase("R1")) {
        digitalWrite(RELAY1_PIN, LOW);   // activa relé
        Serial.println(F("Relé 1 ACTIVADO"));
      } else if (linea.equalsIgnoreCase("R1OFF")) {
        digitalWrite(RELAY1_PIN, HIGH);  // desactiva relé
        Serial.println(F("Relé 1 DESACTIVADO"));
      } else if (linea.equalsIgnoreCase("R2")) {
        digitalWrite(RELAY2_PIN, LOW);
        Serial.println(F("Relé 2 ACTIVADO"));
      } else if (linea.equalsIgnoreCase("R2OFF")) {
        digitalWrite(RELAY2_PIN, HIGH);
        Serial.println(F("Relé 2 DESACTIVADO"));
      } else if (linea.equalsIgnoreCase("RALL")) {
        digitalWrite(RELAY1_PIN, LOW);
        digitalWrite(RELAY2_PIN, LOW);
        Serial.println(F("Relés 1 y 2 ACTIVADOS"));
      } else if (linea.equalsIgnoreCase("RALLOFF")) {
        digitalWrite(RELAY1_PIN, HIGH);
        digitalWrite(RELAY2_PIN, HIGH);
        Serial.println(F("Relés 1 y 2 DESACTIVADOS"));
      } else {
        Serial.println(F("Comando invalido"));
      }

      imprimir();
      linea = "";
    } else {                               // acumula caracteres
      linea += c;
      if (linea.length() > 16) linea = "";
    }
  }
}