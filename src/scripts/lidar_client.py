from rplidar import RPLidar, RPLidarException
import os
import time
import socketio
import threading

print("SCRIPT LIDAR")

sio = socketio.Client()
project_root = os.getenv('PROJECT_ROOT', '')
port_com_lidar = os.getenv('PORT_LIDAR', '/dev/rplidar')
sensor_distance = 0
sensor_angle = 0

sensor_mode = 0

def read_sensor_distance():
    global sensor_distance
    try:
        with open(f"{project_root}/status/lidar_distance.txt", "r") as file:
            new_distance = file.read().strip()
            if new_distance != str(sensor_distance):
                sensor_distance = int(new_distance)
                print(f"Distancia actualizada a {sensor_distance}")
    except Exception as e:
        print(f"Error al leer el archivo lidar_distance.txt: {e}")


def read_sensor_angle():
    global sensor_angle
    try:
        with open(f"{project_root}/status/lidar_angle.txt", "r") as file:
            new_angle = file.read().strip()
            if new_angle != str(sensor_angle):
                sensor_angle = int(new_angle)
                print(f"Ángulo actualizado a {sensor_angle}")
    except Exception as e:
        print(f"Error al leer el archivo lidar_angle.txt: {e}")


def read_sensor_mode():
    global sensor_mode
    try:
        with open(f"{project_root}/status/lidar_status.txt", "r") as file:
            new_mode = file.read().strip()
            if new_mode != str(sensor_mode):
                sensor_mode = int(new_mode)
                print(f"Modo actualizado a {sensor_mode}")
    except Exception as e:
        print(f"Error al leer el archivo lidar_status.txt: {e}")


def monitor_mode_changes():
    global sensor_mode
    while True:
        read_sensor_distance()
        read_sensor_angle()
        read_sensor_mode()
        time.sleep(5)


def notificar_maestro(distance, angle):
    global sensor_distance, sensor_angle
    half_range_angle = sensor_angle / 2
    if (angle >= (360 - half_range_angle) or angle <= half_range_angle) and distance < sensor_distance:
        # print(f"Objeto detectado a {distance} mm en el ángulo {angle} grados")
        sio.emit('sensor_data', {'sensor': 'lidar', 'distance': distance, 'angle': angle})

def main():
    global lidar, sensor_mode
    mode_thread = threading.Thread(target=monitor_mode_changes)
    mode_thread.daemon = True
    mode_thread.start()

    read_sensor_distance()
    read_sensor_angle()
    read_sensor_mode()
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            lidar = RPLidar(port_com_lidar, 256000)
            
            time.sleep(2)
            
            info = lidar.get_info()
            print("LIDAR Info:", info)
            
            print("Starting spinning .......\n")
            lidar.start_motor()
            time.sleep(5)  # Dar tiempo para que el motor alcance velocidad
            
            health = lidar.get_health()
            if health[0] != 'Good':
                raise RPLidarException('Lidar not healthy')
                
            print("Scanning started\n")

            for scan in lidar.iter_scans():
                if sensor_mode == 1:
                    for (_, angle, distance) in scan:
                        notificar_maestro(distance, angle)
            

        except RPLidarException as e:
            print(f"Error del LIDAR: {e}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"Reintentando conexión ({retry_count}/{max_retries})...")
                time.sleep(2)
                try:
                    lidar.stop()
                    lidar.stop_motor()
                    lidar.disconnect()
                    lidar = RPLidar(port_com_lidar, 256000)
                except:
                    pass
            else:
                print("Número máximo de reintentos alcanzado")
                break
        finally:
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()


@sio.event
def connect():
    print('Conexión establecida con el servidor Socket.IO')
    main()


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
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            print("Programa detenido por el usuario")
            break