import os
import subprocess
import time
from pymavlink import mavutil
import threading

print("script: LATENCY starting...")


session_name = os.getenv('SCREEN_SESSION_NAME', "mavproxy_session")
ip_local_mavproxy = os.getenv('IP_LOCAL_MAVPROXY', '0.0.0.0')
host_to_ping = os.getenv('IP_REMOTE_MAVPROXY', '192.168.18.20')
connection_string = f"udp:{ip_local_mavproxy}:14551"
master = mavutil.mavlink_connection(connection_string)
max_latency = 800


def send_command_to_wsl(command):
    wsl_command = f'screen -S {session_name} -p 0 -X stuff "{command}\\n"'
    subprocess.run(wsl_command, shell=True)


def execute_commands():
    print("Send command")
    commands = [
        'rc 2 2000',
        'rc 2 0',
        'mode hold',
    ]
    
    for command in commands:
        send_command_to_wsl(command)


def execute_commands_in_thread():
    command_thread = threading.Thread(target=execute_commands)
    command_thread.start()


def check_ping(host):
    try:
        output = subprocess.check_output(["ping", "-n", "1", "-w", "2000", host], timeout=8)
        lines = output.decode().strip().split("\n")
        for line in lines:
            if "time=" in line:
                time_ms = line.split("time=")[-1].split(" ")[0]
                time_ms = float(time_ms.replace('ms', ''))
                return time_ms
    except subprocess.CalledProcessError:
        print(f"No se puede hacer ping a {host}.")
    except subprocess.TimeoutExpired:
        print(f"Tiempo de espera de ping agotado para {host}.")
    except ValueError:
        print("Error al convertir el tiempo a float.")
    return None


def get_current_mode():
    master.wait_heartbeat()
    mode = master.recv_match(type='HEARTBEAT', blocking=True)
    return mode.custom_mode  # Devuelve el modo actual como un entero


while True:
    ping_time = check_ping(host_to_ping)
    
    if ping_time is not None:
        print(f"Ping a {host_to_ping}: {ping_time} ms")
        
        if ping_time > max_latency:
            current_mode = get_current_mode()
            print(f"Modo actual: {current_mode}")
            
            if current_mode != 4:
                print("Ping alto, cambiando el estado a HOLD...")
                execute_commands_in_thread()
            else:
                print("Ya está en modo HOLD.")
        else:
            print("Ping en rango aceptable.")
    else:
        print("Conexión perdida, ejecutando comandos...")
        execute_commands_in_thread()
    
    time.sleep(2) 
