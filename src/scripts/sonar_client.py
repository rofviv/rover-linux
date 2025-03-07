import socket
import os
import time
import serial
import threading
from datetime import datetime

print("SCRIPT SONAR")

project_root = os.getenv('PROJECT_ROOT', '')
port_arduino = os.getenv('PORT_ARDUINO', '/dev/arduino')
arduino = serial.Serial(port=port_arduino, baudrate=9600, timeout=1)
arduino.reset_input_buffer()

sensor_front_status = 1
sensor_back_status = 0
sensor_front_distance = 20
sensor_back_distance = 80


def read_sensor_front_status():
    global sensor_front_status
    try:
        with open(f"{project_root}/status/sonar_front_status.txt", "r") as file:
            mode = file.read().strip()
            sensor_front_status = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo sonar_front_status.txt: {e}")


def read_sensor_back_status():
    global sensor_back_status
    try:
        with open(f"{project_root}/status/sonar_back_status.txt", "r") as file:
            mode = file.read().strip()
            sensor_back_status = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo sonar_back_status.txt: {e}")


def read_sensor_front_distance():
    global sensor_front_distance
    try:
        with open(f"{project_root}/status/sonar_front_distance.txt", "r") as file:
            mode = file.read().strip()
            sensor_front_distance = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo sonar_front_distance.txt: {e}")


def read_sensor_back_distance():
    global sensor_back_distance
    try:
        with open(f"{project_root}/status/sonar_back_distance.txt", "r") as file:
            mode = file.read().strip()
            sensor_back_distance = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo sonar_back_distance.txt: {e}")



def monitor_mode_changes():
    global sensor_front_status
    while True:
        read_sensor_front_status()
        read_sensor_back_status()
        read_sensor_front_distance()
        read_sensor_back_distance()
        time.sleep(5)


def manejar_sensor(sensor, distancia, max_distance):
    if distancia < max_distance:
        notificar_maestro(f"sonar-{sensor}")
        print(f"Sensor sonar-{sensor} detecta objeto a {distancia} cm")


def leer_sensor():
    mode_thread = threading.Thread(target=monitor_mode_changes)
    mode_thread.daemon = True
    mode_thread.start()
    read_sensor_front_status()
    read_sensor_back_status()
    read_sensor_front_distance()
    read_sensor_back_distance()
    print(f"Sonar Status: {sensor_front_status}")
    print(f"Sonar Status Mode Back: {sensor_back_status}")
    print(f"Sonar Distance: {sensor_front_distance}")
    print(f"Sonar Distance Mode Back: {sensor_back_distance}")


    try:
        while True:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8').strip()
                try:
                    if sensor_front_status == 1:
                        datos = linea.split(',')
                        sensor = int(datos[0])
                        distancia = float(datos[1])

                        current_time = datetime.now().strftime('%H:%M:%S')
                        print(f"{current_time} - {linea}")

                        # manejar_sensor(sensor, distancia, sensor_front_distance)
                        if sensor_back_status == 1:
                            if sensor == 4:
                                manejar_sensor(sensor, distancia, sensor_back_distance)
                        elif sensor != 4:
                            manejar_sensor(sensor, distancia, sensor_front_distance)
                except (IndexError, ValueError):
                    print("Error al procesar los datos del sensor")

            time.sleep(0.1)
    except Exception as e:
        print(f"Error en la lectura del sensor: {e}")
    finally:
        print('arduino close')
        arduino.close()


def notificar_maestro(mensaje):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 65432))
            s.sendall(mensaje.encode('utf-8'))
            print(f'Notificación "{mensaje}" enviada al maestro.')
    except ConnectionRefusedError:
        print('No se pudo conectar con el maestro. Reintentando...')


if __name__ == "__main__":
    try:
        leer_sensor()
    except KeyboardInterrupt:
        print("Programa detenido por el usuario")
    finally:
        if arduino.is_open:
            arduino.close()

