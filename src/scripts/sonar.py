import RPi.GPIO as GPIO
import time

print("script: SONAR SENSOR starting...")

# Definimos los pines de los sensores
num_sensores = 1  # Número de sensores que vas a usar
echo_pins = [12]  # Pines Echo (BCM)
trig_pins = [13]  # Pines Trig (BCM)
distancias = [0] * num_sensores  # Array para almacenar distancias

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BCM)  # Usamos el esquema BCM
for i in range(num_sensores):
    GPIO.setup(trig_pins[i], GPIO.OUT)
    GPIO.setup(echo_pins[i], GPIO.IN)
    GPIO.output(trig_pins[i], GPIO.LOW)

# Función para medir la distancia
def medir_distancia(sensor_index):
    GPIO.output(trig_pins[sensor_index], GPIO.LOW)
    time.sleep(0.002)
    GPIO.output(trig_pins[sensor_index], GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pins[sensor_index], GPIO.LOW)

    while GPIO.input(echo_pins[sensor_index]) == 0:
        inicio_pulso = time.time()

    while GPIO.input(echo_pins[sensor_index]) == 1:
        fin_pulso = time.time()

    duracion = fin_pulso - inicio_pulso
    distancia = duracion * 34300 / 2  # Convertimos a centímetros
    return distancia

# Loop principal
try:
    while True:
        for i in range(num_sensores):
            distancias[i] = medir_distancia(i)  # Medimos la distancia para cada sensor

            if distancias[i] < 80:  # Si detecta algo a menos de 80 cm
                print(f"Sensor {i + 1}, Distancia: {distancias[i]:.2f} cm")

        time.sleep(0.3)  # Esperamos 300 ms antes de la siguiente medición

except KeyboardInterrupt:
    print("Programa interrumpido")

finally:
    GPIO.cleanup()  # Restablecemos los pines GPIO
