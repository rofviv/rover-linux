from rplidar import RPLidar, RPLidarException
import os
import time
import socket
import threading

print("SCRIPT LIDAR")

project_root = os.getenv('PROJECT_ROOT', '')
port_com_lidar = os.getenv('PORT_LIDAR', '/dev/rplidar')
sensor_distance = 1700
sensor_angle = 30
# half_range_angle = range_angle / 2
min_angle = 0.0
max_angle = 359.9

sensor_mode = 1

def read_sensor_distance():
    global sensor_distance
    try:
        with open(f"{project_root}/status/lidar_distance.txt", "r") as file:
            sensor_distance = file.read().strip()
            sensor_distance = int(sensor_distance)
    except Exception as e:
        print(f"Error al leer el archivo lidar_distance.txt: {e}")


def read_sensor_angle():
    global sensor_angle
    try:
        with open(f"{project_root}/status/lidar_angle.txt", "r") as file:
            mode = file.read().strip()
            sensor_angle = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo lidar_angle.txt: {e}")

def read_sensor_mode():
    global sensor_mode
    try:
        with open(f"{project_root}/status/lidar_status.txt", "r") as file:
            mode = file.read().strip()
            sensor_mode = int(mode)
    except Exception as e:
        print(f"Error al leer el archivo lidar_status.txt: {e}")


def monitor_mode_changes():
    global sensor_mode
    while True:
        read_sensor_distance()
        read_sensor_angle()
        read_sensor_mode()
        time.sleep(5)


def notificar_maestro(mensaje):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 65432))
            s.sendall(mensaje.encode('utf-8'))
            print(f'Notificación "{mensaje}" enviada al maestro.')
    except ConnectionRefusedError:
        print('No se pudo conectar con el maestro. Reintentando...')


def main():
    global lidar
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
            
            # Verificar la conexión antes de continuar
            health = lidar.get_health()
            if health[0] != 'Good':
                raise RPLidarException('Lidar not healthy')
                
            print("Scanning started\n")
            print(f"Range distance = {sensor_distance}")

            for scan in lidar.iter_scans():
                half_range_angle = sensor_angle / 2
                for (_, angle, distance) in scan:
                    if (angle >= (max_angle - half_range_angle) or angle <= (min_angle + half_range_angle)) and distance < sensor_distance:
                        if sensor_mode == 1:
                            print(f"Objeto detectado a {distance} mm en el ángulo {angle} grados")
                            print("Ejecutando comandos en segundo plano...\n")
                            notificar_maestro("lidar")
                        break
            
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

if __name__ == "__main__":
    main()
