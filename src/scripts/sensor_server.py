import socket
import os
import subprocess
import time
import threading

print("SCRIPT SENSOR SERVER MAVPROXY")

TIEMPO_MAX_ESPERA = 2
session_name = os.getenv('SESSION_NAME', "mavproxy_session")
rc_channel_number_start = os.getenv('RC_CHANNEL_NUMBER_START', '6')
rc_channel_number_stop = os.getenv('RC_CHANNEL_NUMBER_STOP', '2')
ip_remote_mavproxy = os.getenv('IP_REMOTE_MAVPROXY', '192.168.18.20')
port = ":14550"
add_command = True

ultimo_tiempo_deteccion = {"sonar-1": time.time(), "sonar-2": time.time(), "sonar-3": time.time(), "sonar-4": time.time(), "lidar": time.time()}
estado_sensores = {"sonar-1": False, "sonar-2": False, "sonar-3": False, "sonar-4": False, "lidar": False}

commands_rover = {
    "stop": [
        f'rc {rc_channel_number_start} 1005',
        f'rc {rc_channel_number_stop} 1990',
        f'rc {rc_channel_number_start} 0',
        f'rc {rc_channel_number_stop} 0'
    ],
    "add": [
        f'output add {ip_remote_mavproxy}{port}',
    ]
}


def send_command_to_wsl(command):
    wsl_command = f'screen -S {session_name} -p 0 -X stuff "{command}\\n"'
    try:
        subprocess.run(wsl_command, shell=True)
    except Exception as e:
        print(f"Error al enviar comando a Screen: {e}")


def execute_command(commands):
    send_command_to_wsl("output remove 1")
    time.sleep(0.1)
    for command in commands:
        send_command_to_wsl(command)
        time.sleep(0.1)



def listen_sensors(sensor):
    global estado_sensores, ultimo_tiempo_deteccion, add_command

    ultimo_tiempo_deteccion[sensor] = time.time()
    if not estado_sensores[sensor]:
        estado_sensores[sensor] = True
        print(f"ejecutar comando {sensor}")
        add_command = False
        execute_command(commands_rover["stop"])


def verificar_sensores_timeout():
    global estado_sensores, ultimo_tiempo_deteccion, add_command

    tiempo_actual = time.time()

    for sensor in estado_sensores.keys():
        if estado_sensores[sensor] and (tiempo_actual - ultimo_tiempo_deteccion[sensor]) > TIEMPO_MAX_ESPERA:
            estado_sensores[sensor] = False
            print(f"sensor {sensor} false")

    check_object = any(estado_sensores[sensor] for sensor in estado_sensores.keys())

    if not check_object:
        if not add_command:
            print("ejecutar comando add")
            execute_command(commands_rover["add"])
            add_command = True


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))  # Puedes cambiar el puerto si lo deseas
    server_socket.listen()

    print('Waiting data sensors...')
    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f'Received {addr}')
            data = conn.recv(1024).decode('utf-8')
            if data:
                listen_sensors(data)

def start_timeout_verification():
    while True:
        verificar_sensores_timeout()
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=start_timeout_verification, daemon=True).start()
    start_server()
