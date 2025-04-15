# pip install flask-socketio==5.5.1
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import requests
import os
import subprocess
import time
import threading


print("SCRIPT ROVER API - SOCKETIO")

PROJECT_ROOT = os.environ.get('PROJECT_ROOT', os.getcwd())
IP_RELAY_FILE = os.path.join(PROJECT_ROOT, 'status', 'ip_relay.txt')
TOKEN_FILE = os.path.join(PROJECT_ROOT, 'status', 'token.txt')
LATENCY_STATUS_FILE = os.path.join(PROJECT_ROOT, 'status', 'latency_status.txt')
LIDAR_STATUS_FILE = os.path.join(PROJECT_ROOT, 'status', 'lidar_status.txt')
SONAR_BACK_STATUS_FILE = os.path.join(PROJECT_ROOT, 'status', 'sonar_back_status.txt')
SONAR_FRONT_STATUS_FILE = os.path.join(PROJECT_ROOT, 'status', 'sonar_front_status.txt')
SONAR_BACK_DISTANCE_FILE = os.path.join(PROJECT_ROOT, 'status', 'sonar_back_distance.txt')
SONAR_FRONT_DISTANCE_FILE = os.path.join(PROJECT_ROOT, 'status', 'sonar_front_distance.txt')
LIDAR_DISTANCE_FILE = os.path.join(PROJECT_ROOT, 'status', 'lidar_distance.txt')
LIDAR_ANGLE_FILE = os.path.join(PROJECT_ROOT, 'status', 'lidar_angle.txt')
LATENCY_TIME_FILE = os.path.join(PROJECT_ROOT, 'status', 'latency_time_ms.txt')
SESSION_NAME = os.getenv('SESSION_NAME', "mavproxy_session")
IP_REMOTE_MAVPROXY = os.getenv('IP_REMOTE_MAVPROXY', '192.168.18.1')
RC_CHANNEL_NUMBER_START = os.getenv('RC_CHANNEL_NUMBER_START', '6')
RC_CHANNEL_NUMBER_STOP = os.getenv('RC_CHANNEL_NUMBER_STOP', '2')

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
connected_clients = {}

commands_rover = {
    "neutral": [
        f'rc {RC_CHANNEL_NUMBER_START} 1500',
        f'rc {RC_CHANNEL_NUMBER_START} 0'
    ],
    "brake": [
        f'rc {RC_CHANNEL_NUMBER_STOP} 1000',
        f'rc {RC_CHANNEL_NUMBER_STOP} 0'
    ],
    "add": [
        f'output add {IP_REMOTE_MAVPROXY}:14550'
    ]
}

## ROUTES API
@app.route('/')
def index():
    return jsonify(success=True, message="Rover API", ip_relay=read_file(IP_RELAY_FILE), token=read_file(TOKEN_FILE), latency_status=read_file(LATENCY_STATUS_FILE), lidar_status=read_file(LIDAR_STATUS_FILE), sonar_back_status=read_file(SONAR_BACK_STATUS_FILE), sonar_front_status=read_file(SONAR_FRONT_STATUS_FILE), sonar_back_distance=read_file(SONAR_BACK_DISTANCE_FILE), sonar_front_distance=read_file(SONAR_FRONT_DISTANCE_FILE), lidar_distance=read_file(LIDAR_DISTANCE_FILE), lidar_angle=read_file(LIDAR_ANGLE_FILE), latency_time=read_file(LATENCY_TIME_FILE))


@app.route('/set_ip_relay', methods=['POST'])
def set_ip_relay():
    data = request.get_json()
    ip_relay = data.get('ip_relay')
    set_file(IP_RELAY_FILE, ip_relay)
    return jsonify(success=True, message="IP relay set", ip_relay=read_file(IP_RELAY_FILE))


@app.route('/read_ip_relay', methods=['GET'])
def read_ip_relay():
    return jsonify(success=True, message="IP relay read", ip_relay=read_file(IP_RELAY_FILE))


@app.route('/sync_data_relay', methods=['GET'])
def sync_data_relay():
    try:
        data = requests.get(f"http://{read_file(IP_RELAY_FILE)}", timeout=8)
        return jsonify(success=True, message="Data relay sync", data=data.json())
    except requests.Timeout:
        return jsonify(success=False, message="Timeout error - Error al sincronizar los datos")
    except Exception as e:
        return jsonify(success=False, message="Error al sincronizar los datos", error=str(e))


@app.route('/toggle_data_relay', methods=['POST'])
def toggle_data_relay():
    body = request.get_json()
    relay_id = body.get('relay_id')
    try:
        requests.post(f"http://{read_file(IP_RELAY_FILE)}/relay{relay_id}", json=body, timeout=8)
        data = requests.get(f"http://{read_file(IP_RELAY_FILE)}")
        return jsonify(success=True, message="Data relay set", data=data.json())
    except requests.Timeout:
        return jsonify(success=False, message="Timeout error - Error al establecer los datos")
    except Exception as e:
        return jsonify(success=False, message="Error al establecer los datos", error=str(e))
    

@app.route('/set_token', methods=['POST'])
def set_token():
    data = request.get_json()
    token = data.get('token')
    set_file(TOKEN_FILE, token)
    return jsonify(success=True, message="Token set", token=read_file(TOKEN_FILE))


@app.route('/read_token', methods=['GET'])
def read_token():
    return jsonify(success=True, message="Token read", token=read_file(TOKEN_FILE))


@app.route('/set_latency_status', methods=['POST'])
def set_latency_status():
    data = request.get_json()
    latency_status = data.get('latency_status')
    set_file(LATENCY_STATUS_FILE, latency_status)
    return jsonify(success=True, message="Latency status set", latency_status=read_file(LATENCY_STATUS_FILE))


@app.route('/read_latency_status', methods=['GET'])
def read_latency_status():
    return jsonify(success=True, message="Latency status read", latency_status=read_file(LATENCY_STATUS_FILE))


@app.route('/set_lidar_status', methods=['POST'])
def set_lidar_status():
    data = request.get_json()
    lidar_status = data.get('lidar_status')
    set_file(LIDAR_STATUS_FILE, lidar_status)
    return jsonify(success=True, message="Lidar status set", lidar_status=read_file(LIDAR_STATUS_FILE))


@app.route('/read_lidar_status', methods=['GET'])
def read_lidar_status():
    return jsonify(success=True, message="Lidar status read", lidar_status=read_file(LIDAR_STATUS_FILE))


@app.route('/set_sonar_back_status', methods=['POST'])
def set_sonar_back_status():
    data = request.get_json()
    sonar_back_status = data.get('sonar_back_status')
    set_file(SONAR_BACK_STATUS_FILE, sonar_back_status)
    return jsonify(success=True, message="Sonar back status set", sonar_back_status=read_file(SONAR_BACK_STATUS_FILE))


@app.route('/read_sonar_back_status', methods=['GET'])
def read_sonar_back_status():
    return jsonify(success=True, message="Sonar back status read", sonar_back_status=read_file(SONAR_BACK_STATUS_FILE))


@app.route('/set_sonar_front_status', methods=['POST'])
def set_sonar_front_status():
    data = request.get_json()
    sonar_front_status = data.get('sonar_front_status')
    set_file(SONAR_FRONT_STATUS_FILE, sonar_front_status)
    return jsonify(success=True, message="Sonar front status set", sonar_front_status=read_file(SONAR_FRONT_STATUS_FILE))


@app.route('/read_sonar_front_status', methods=['GET'])
def read_sonar_front_status():
    return jsonify(success=True, message="Sonar front status read", sonar_front_status=read_file(SONAR_FRONT_STATUS_FILE))


@app.route('/set_sonar_back_distance', methods=['POST'])
def set_sonar_back_distance():
    data = request.get_json()
    sonar_back_distance = data.get('sonar_back_distance')
    set_file(SONAR_BACK_DISTANCE_FILE, sonar_back_distance)
    return jsonify(success=True, message="Sonar back distance set", sonar_back_distance=read_file(SONAR_BACK_DISTANCE_FILE))


@app.route('/read_sonar_back_distance', methods=['GET'])
def read_sonar_back_distance():
    return jsonify(success=True, message="Sonar back distance read", sonar_back_distance=read_file(SONAR_BACK_DISTANCE_FILE))


@app.route('/set_sonar_front_distance', methods=['POST'])
def set_sonar_front_distance():
    data = request.get_json()
    sonar_front_distance = data.get('sonar_front_distance')
    set_file(SONAR_FRONT_DISTANCE_FILE, sonar_front_distance)
    return jsonify(success=True, message="Sonar front distance set", sonar_front_distance=read_file(SONAR_FRONT_DISTANCE_FILE))


@app.route('/read_sonar_front_distance', methods=['GET'])
def read_sonar_front_distance():
    return jsonify(success=True, message="Sonar front distance read", sonar_front_distance=read_file(SONAR_FRONT_DISTANCE_FILE))


@app.route('/set_lidar_distance', methods=['POST'])
def set_lidar_distance():
    data = request.get_json()
    lidar_distance = data.get('lidar_distance')
    set_file(LIDAR_DISTANCE_FILE, lidar_distance)
    return jsonify(success=True, message="Lidar distance set", lidar_distance=read_file(LIDAR_DISTANCE_FILE))


@app.route('/read_lidar_distance', methods=['GET'])
def read_lidar_distance():
    return jsonify(success=True, message="Lidar distance read", lidar_distance=read_file(LIDAR_DISTANCE_FILE))


@app.route('/set_lidar_angle', methods=['POST'])
def set_lidar_angle():
    data = request.get_json()
    lidar_angle = data.get('lidar_angle')
    set_file(LIDAR_ANGLE_FILE, lidar_angle)
    return jsonify(success=True, message="Lidar angle set", lidar_angle=read_file(LIDAR_ANGLE_FILE))    


@app.route('/read_lidar_angle', methods=['GET'])
def read_lidar_angle():
    return jsonify(success=True, message="Lidar angle read", lidar_angle=read_file(LIDAR_ANGLE_FILE))


@app.route('/set_latency_time', methods=['POST'])
def set_latency_time():
    data = request.get_json()
    latency_time = data.get('latency_time')
    set_file(LATENCY_TIME_FILE, latency_time)
    return jsonify(success=True, message="Latency time set", latency_time=read_file(LATENCY_TIME_FILE))


@app.route('/read_latency_time', methods=['GET'])
def read_latency_time():
    return jsonify(success=True, message="Latency time read", latency_time=read_file(LATENCY_TIME_FILE))


@app.route('/execute_screen/<screen_name>', methods=['POST'])
def execute_screen(screen_name):
    if not screen_name:
        return jsonify({
            'success': False,
            'error': 'Screen name is required'
        })

    try:
        script_path = f'{PROJECT_ROOT}/launcher/{screen_name}.sh'
        
        if not os.path.exists(script_path):
            return jsonify({
                'success': False, 
                'error': f'Script {screen_name}.sh not found'
            })

        result = subprocess.run(['bash', script_path], capture_output=False, text=True)
        
        return jsonify({
            'success': True,
            'output': f'{screen_name} executed',
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


## SOCKETIO EVENTS
@socketio.on('connect')
def connect():
    ip = request.remote_addr
    connected_clients[ip] = {'connected': True, 'timestamp': time.time()}
    print('Client connected')


@socketio.on('disconnect')
def disconnect(reason):
    ip = request.remote_addr
    connected_clients[ip]['timestamp'] = time.time() - 2
    print(f'Client {ip} disconnected')


@socketio.on('sensor_data')
def sensor_data(data):
    print('message received with ', data)

    if not is_remote_ip_connected():
        print("Remote IP not connected STOP")
        execute_command(commands_rover["neutral"])
        execute_command(commands_rover["brake"])

    emit('sensor_data', data, broadcast=True)


@socketio.on('cube_data')
def cube_data(data):
    emit('cube_data', data, broadcast=True)


@socketio.on('latency')
def latency(data):
    print('message received with ', data)
    emit('latency', data, broadcast=True)


@socketio.on('heartbeat')
def on_heartbeat(data):
    ip = request.remote_addr
    connected_clients[ip] = {'connected': True, 'timestamp': time.time()}


## FUNCTIONS
def read_file(file_path) -> str | None:
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error al leer el archivo {file_path}: {e}")


def set_file(file_path, content) -> None:
    with open(file_path, "w") as f:
        f.write(content)
    print(f"File {file_path} set to {content}")


def is_remote_ip_connected() -> bool:
    return connected_clients.get(IP_REMOTE_MAVPROXY, {}).get('connected', False)


def monitor_heartbeats() -> None:
    while True:
        now = time.time()
        for ip, last in list(connected_clients.items()):
            if now - last['timestamp'] > 2 and last['connected']:
                connected_clients[ip]['connected'] = False
                print(f"Cliente {ip} sin comunicación desde hace {int(now - last['timestamp'])}s. Posible desconexión.")
                if ip == IP_REMOTE_MAVPROXY:
                    execute_command(commands_rover["neutral"])
        time.sleep(1)


def execute_command(commands):
    print("execute_command", commands)
    for command in commands:
        send_command_to_rover(command)
        time.sleep(0.1)


def send_command_to_rover(command):
    global SESSION_NAME

    wsl_command = f'screen -S {SESSION_NAME} -p 0 -X stuff "{command}\\n"'
    try:
        subprocess.run(wsl_command, shell=True)
    except Exception as e:
        print(f"Error al enviar comando a Screen: {e}")


## MAIN
if __name__ == '__main__':
    threading.Thread(target=monitor_heartbeats, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

