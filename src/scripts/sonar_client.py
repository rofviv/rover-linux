import os
import time
import serial
import threading
import socketio
from datetime import datetime, timedelta

print("SCRIPT SONAR")

sio = socketio.Client()
project_root = os.getenv('PROJECT_ROOT', '')
port_arduino = os.getenv('PORT_ARDUINO', '/dev/arduino')
arduino = serial.Serial(port=port_arduino, baudrate=9600, timeout=1)
arduino.reset_input_buffer()

sensor_front_status = 0
sensor_back_status = 0
sensor_front_distance = 0
sensor_back_distance = 0

last_time_detection = datetime.now()
is_detection = False

def read_sensor_front_status():
    global sensor_front_status
    try:
        with open(f"{project_root}/status/sonar_front_status.txt", "r") as file:
            mode = file.read().strip()
            if mode != str(sensor_front_status):
                sensor_front_status = int(mode)
                print(f"Estado del sensor frontal actualizado a {sensor_front_status}")
    except Exception as e:
        print(f"Error al leer el archivo sonar_front_status.txt: {e}")


def read_sensor_back_status():
    global sensor_back_status
    try:
        with open(f"{project_root}/status/sonar_back_status.txt", "r") as file:
            mode = file.read().strip()
            if mode != str(sensor_back_status):
                sensor_back_status = int(mode)
                print(f"Estado del sensor trasero actualizado a {sensor_back_status}")
    except Exception as e:
        print(f"Error al leer el archivo sonar_back_status.txt: {e}")


def read_sensor_front_distance():
    global sensor_front_distance
    try:
        with open(f"{project_root}/status/sonar_front_distance.txt", "r") as file:
            new_distance = file.read().strip()
            if new_distance != str(sensor_front_distance):
                sensor_front_distance = int(new_distance)
                print(f"Distancia actualizada a {sensor_front_distance}")
    except Exception as e:
        print(f"Error al leer el archivo sonar_front_distance.txt: {e}")


def read_sensor_back_distance():
    global sensor_back_distance
    try:
        with open(f"{project_root}/status/sonar_back_distance.txt", "r") as file:
            new_distance = file.read().strip()
            if new_distance != str(sensor_back_distance):
                sensor_back_distance = int(new_distance)
                print(f"Distancia actualizada a {sensor_back_distance}")
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


def leer_sensor():
    mode_thread = threading.Thread(target=monitor_mode_changes)
    mode_thread.daemon = True
    mode_thread.start()
    read_sensor_front_status()
    read_sensor_back_status()
    read_sensor_front_distance()
    read_sensor_back_distance()

    try:
        while True:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8').strip()
                try:
                    datos = linea.split(',')
                    sensor = int(datos[0])
                    distancia = float(datos[1])

                    current_time = datetime.now().strftime('%H:%M:%S')
                    print(f"{current_time} - {linea}")
                    notificar_maestro(f"sonar-{sensor}", distancia)

                except (IndexError, ValueError):
                    print("Error al procesar los datos del sensor")

            time.sleep(0.1)
    except Exception as e:
        print(f"Error en la lectura del sensor: {e}")
    finally:
        print('arduino close')
        arduino.close()


def notificar_maestro(sensor, distance):
    global last_time_detection, is_detection
    
    try:
        if sensor == 'sonar-4' and sensor_back_status == 0:
            return
        elif sensor != 'sonar-4' and sensor_front_status == 0:
            return
        
        if sensor == 'sonar-4' and distance > sensor_back_distance:
            return
        elif sensor != 'sonar-4' and distance > sensor_front_distance:
            return
        
        if distance > 0:
            last_time_detection = datetime.now()
            is_detection = True
        sio.emit('sensor_data', {'sensor': sensor, 'distance': distance})
    except ConnectionRefusedError:
        print('No se pudo conectar con el maestro. Reintentando...')


def verificar_timeout():
    global last_time_detection, is_detection
    while True:
        if datetime.now() - last_time_detection > timedelta(milliseconds=1500) and is_detection:
            notificar_maestro('sonar-1', 0)
            notificar_maestro('sonar-2', 0)
            notificar_maestro('sonar-3', 0)
            notificar_maestro('sonar-4', 0)
            is_detection = False
        time.sleep(0.5)


@sio.event
def connect():
    print('Conexión establecida con el servidor Socket.IO')
    threading.Thread(target=verificar_timeout, daemon=True).start()
    leer_sensor()


@sio.event
def disconnect():
    print('Desconectado del servidor Socket.IO')


if __name__ == "__main__":
    while True:
        try:
            print("Intentando conectar al servidor Socket.IO...")
            sio.connect('http://localhost:5000')
            sio.wait()
            break
        except socketio.exceptions.ConnectionError:
            print("No se pudo conectar al servidor. Reintentando en 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Programa detenido por el usuario")
            if arduino.is_open:
                arduino.close()
            break

