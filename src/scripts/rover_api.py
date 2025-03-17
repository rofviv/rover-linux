from flask import Flask, request, jsonify
import requests
import os


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

app = Flask(__name__)

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


def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error al leer el archivo {file_path}: {e}")


def set_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)
    print(f"File {file_path} set to {content}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

