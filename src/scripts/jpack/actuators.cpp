#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver servos = Adafruit_PWMServoDriver(0x40);

// Pines del L298N
const int IN1 = 9;
const int IN2 = 10;

// Pines para relevadores
const int RELAY_RIGHT_TURN = 2;
const int RELAY_LEFT_TURN  = 3;
const int RELAY_REV1       = 4;
const int RELAY_REV2       = 5;
const int RELAY_CHARGE = 6;
// Pulsos para 0° a 180°
unsigned int pos0 = 102;
unsigned int pos180 = 537;

void setServoAngle(uint8_t servoNum, float angle) {
  if (angle < 0) angle = 0;
  if (angle > 180) angle = 180;
  int pulse = map(angle, 0, 180, pos0, pos180);
  servos.setPWM(servoNum, 0, pulse);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  servos.begin();
  servos.setPWMFreq(50);

//   for (int i = 0; i < 4; i++) {
//     setServoAngle(i, 0);
//   }

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  pinMode(RELAY_RIGHT_TURN, OUTPUT);
  pinMode(RELAY_LEFT_TURN, OUTPUT);
  pinMode(RELAY_REV1, OUTPUT);
  pinMode(RELAY_REV2, OUTPUT);
  pinMode(RELAY_CHARGE, OUTPUT);
  
  digitalWrite(RELAY_CHARGE, LOW);
  digitalWrite(RELAY_RIGHT_TURN, LOW);
  digitalWrite(RELAY_LEFT_TURN, LOW);
  digitalWrite(RELAY_REV1, LOW);
  digitalWrite(RELAY_REV2, LOW);

  Serial.println("Sistema listo.");
  Serial.println("Comandos:");
  Serial.println(" - <servo> <ángulo>  (ej: 1 90)");
  Serial.println(" - f = motor adelante | r = reversa | s = stop");
  Serial.println(" - dr on/off, iz on/off, rev1 on/off, rev2 on/off");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    // Comandos de motor DC
    if (input == "f") {
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      Serial.println("Motor adelante");
    } else if (input == "r") {
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      Serial.println("Motor reversa");
    } else if (input == "s") {
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      Serial.println("Motor detenido");
    }
    // Comandos de relés
    else if (input == "dr on") {
      digitalWrite(RELAY_RIGHT_TURN, HIGH);
      Serial.println("Guiñador derecho encendido");
    } else if (input == "dr off") {
      digitalWrite(RELAY_RIGHT_TURN, LOW);
      Serial.println("Guiñador derecho apagado");
    } else if (input == "iz on") {
      digitalWrite(RELAY_LEFT_TURN, HIGH);
      Serial.println("Guiñador izquierdo encendido");
    } else if (input == "iz off") {
      digitalWrite(RELAY_LEFT_TURN, LOW);
      Serial.println("Guiñador izquierdo apagado");
    } else if (input == "rev1 on") {
      digitalWrite(RELAY_REV1, HIGH);
      Serial.println("Reversa motor 1 activada");
    } else if (input == "rev1 off") {
      digitalWrite(RELAY_REV1, LOW);
      Serial.println("Reversa motor 1 desactivada");
    } else if (input == "rev2 on") {
      digitalWrite(RELAY_REV2, HIGH);
      Serial.println("Reversa motor 2 activada");
    } else if (input == "rev2 off") {
      digitalWrite(RELAY_REV2, LOW);
      Serial.println("Reversa motor 2 desactivada");
    } else if (input == "revAll on") {
      digitalWrite(RELAY_REV1, HIGH);
      digitalWrite(RELAY_REV2, HIGH);
      Serial.println("Reversa motor 1 y 2 activada");
    } else if (input == "revAll off") {
      digitalWrite(RELAY_REV1, LOW);
      digitalWrite(RELAY_REV2, LOW);
      Serial.println("Reversa motor 1 y 2 desactivada");
    } else if (input == "charge on") {
      digitalWrite(RELAY_CHARGE, HIGH);
      Serial.println("Carga autónoma activada");
    } else if (input == "charge off") {
      digitalWrite(RELAY_CHARGE, LOW);
      Serial.println("Carga autónoma desactivada");
    }
    // Comando de servo
    else {
      int spaceIndex = input.indexOf(' ');
      if (spaceIndex > 0) {
        int servoNum = input.substring(0, spaceIndex).toInt();
        int angle = input.substring(spaceIndex + 1).toInt();

        if (servoNum >= 0 && servoNum <= 15 && angle >= 0 && angle <= 180) {
          setServoAngle(servoNum, angle);
          Serial.print("Servo ");
          Serial.print(servoNum);
          Serial.print(" movido a ");
          Serial.print(angle);
          Serial.println("°");
        } else {
          Serial.println("Error: Servo (0-15) o ángulo (0-180) fuera de rango.");
        }
      } else {
        Serial.println("Entrada no válida. Ejemplo: 1 90");
      }
    }
  }
}