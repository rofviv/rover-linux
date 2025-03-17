import os
import subprocess
import time
import threading
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

# Variables de entorno
project_root = os.getenv('PROJECT_ROOT', '')
session_name = os.getenv('SCREEN_SESSION_NAME', "mavproxy_session")
rc_channel_number_start = os.getenv('RC_CHANNEL_NUMBER_START', '6')
rc_channel_number_stop = os.getenv('RC_CHANNEL_NUMBER_STOP', '2')
ip_local_mavproxy = os.getenv('IP_LOCAL_MAVPROXY', '0.0.0.0')
host_to_ping = os.getenv('IP_REMOTE_MAVPROXY', '192.168.18.20')
sensor_time = 800
sensor_mode = 1

logger.info("LATENCY Monitor Starting...")

def read_sensor_time():
    global sensor_time
    try:
        with open(f"{project_root}/status/latency_time_ms.txt", "r", encoding='utf-8') as file:
            sensor_time = file.read().strip()
            sensor_time = int(sensor_time)
    except Exception as e:
        logger.error(f"Error reading status/latency_time_ms.txt: {e}")


def read_sensor_mode():
    global sensor_mode
    try:
        with open(f"{project_root}/status/latency_status.txt", "r", encoding='utf-8') as file:
            mode = file.read().strip()
            sensor_mode = int(mode)
    except Exception as e:
        logger.error(f"Error reading status/latency_status.txt: {e}")

def monitor_mode_changes():
    global sensor_mode
    while True:
        read_sensor_mode()
        read_sensor_time()
        time.sleep(5)

def send_command_to_wsl(command):
    wsl_command = f'screen -S {session_name} -p 0 -X stuff "{command}\\n"'
    try:
        subprocess.run(wsl_command, shell=True, check=True)
        logger.debug(f"Command sent: {command}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error sending command to Screen: {e}")

def execute_commands():
    logger.info("Executing emergency commands")
    commands = [
        f'rc {rc_channel_number_start} 1005',
        f'rc {rc_channel_number_stop} 1990',
        f'rc {rc_channel_number_start} 0',
        f'rc {rc_channel_number_stop} 0',
    ]
    
    for command in commands:
        send_command_to_wsl(command)
        time.sleep(0.1)


def execute_commands_in_thread():
    command_thread = threading.Thread(target=execute_commands)
    command_thread.start()

def check_ping(host):
    try:
        output = subprocess.check_output(
            ["ping", "-c", "1", "-W", "2", host],
            timeout=8,
            encoding='utf-8'
        )
        
        for line in output.strip().split("\n"):
            if "time=" in line:
                time_ms = float(line.split("time=")[-1].split(" ")[0].strip())
                return time_ms
                
    except subprocess.CalledProcessError:
        logger.warning(f"Could not ping {host}")
    except subprocess.TimeoutExpired:
        logger.warning(f"Ping timeout for {host}")
    except ValueError as e:
        logger.error(f"Error converting ping time: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during ping: {e}")
    
    return None

def main():
    logger.info("Starting latency monitoring...")
    
    # Iniciar monitoreo de cambios de modo
    mode_thread = threading.Thread(target=monitor_mode_changes)
    mode_thread.daemon = True
    mode_thread.start()

    read_sensor_time()
    read_sensor_mode()

    logger.info(f"Configuration: Host={host_to_ping}, Max Latency={sensor_time}ms")

    while True:
        try:
            ping_time = check_ping(host_to_ping)
            
            if ping_time is not None:
                status = "OK" if ping_time <= sensor_time else "HIGH LATENCY"
                logger.info(f"Latency: {ping_time:.1f}ms | Max: {sensor_time}ms | Mode: {sensor_mode} | Status: {status}")
                
                if ping_time > sensor_time and sensor_mode == 1:
                    logger.warning(f"Latency exceeded threshold: {ping_time:.1f}ms > {sensor_time}ms")
                    execute_commands_in_thread()
            else:
                logger.error(f"Connection lost | Mode: {sensor_mode}")
                if sensor_mode == 1:
                    execute_commands_in_thread()
            
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Main loop error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Latency monitor stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")