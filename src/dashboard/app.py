from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

PROJECT_ROOT = os.environ.get('PROJECT_ROOT', os.getcwd())
SONAR_FRONT_STATUS_FILE = os.path.join(PROJECT_ROOT, 'status', 'sonar_front_status.txt')
SONAR_BACK_STATUS_FILE = os.path.join(PROJECT_ROOT, 'status', 'sonar_back_status.txt')
SONAR_DISTANCE_FILE = os.path.join(PROJECT_ROOT, 'status', 'sonar_distance.txt')
LATENCY_STATUS_FILE = os.path.join(PROJECT_ROOT, 'status', 'latency_status.txt')

def get_sonar_front_status():
    if os.path.exists(SONAR_FRONT_STATUS_FILE):
        with open(SONAR_FRONT_STATUS_FILE, 'r') as f:
            return f.read().strip() == '1'
    return False

def update_sonar_front_status(status):
    with open(SONAR_FRONT_STATUS_FILE, 'w') as f:
        f.write('1' if status else '0')

def get_sonar_back_status():
    if os.path.exists(SONAR_BACK_STATUS_FILE):
        with open(SONAR_BACK_STATUS_FILE, 'r') as f:
            return f.read().strip() == '1'
    return False

def update_sonar_back_status(status):
    with open(SONAR_BACK_STATUS_FILE, 'w') as f:
        f.write('1' if status else '0')

def get_sonar_distance():
    if os.path.exists(SONAR_DISTANCE_FILE):
        with open(SONAR_DISTANCE_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

def update_sonar_distance(distance):
    distance = max(1, min(80, int(distance)))
    with open(SONAR_DISTANCE_FILE, 'w') as f:
        f.write(str(distance))

def get_latency_status():
    if os.path.exists(LATENCY_STATUS_FILE):
        with open(LATENCY_STATUS_FILE, 'r') as f:
            return f.read().strip() == '1'
    return False

def update_latency_status(status):
    with open(LATENCY_STATUS_FILE, 'w') as f:
        f.write('1' if status else '0')

@app.route('/')
def index():
    current_front_status = get_sonar_front_status()
    current_back_status = get_sonar_back_status()
    current_distance = get_sonar_distance()
    current_latency_status = get_latency_status()
    return render_template('index.html', current_front_status=current_front_status, 
                           current_back_status=current_back_status, 
                           current_distance=current_distance,
                           current_latency_status=current_latency_status)

@app.route('/update_sensor', methods=['POST'])
def update_sensor():
    data = request.json
    if 'front_status' in data:
        update_sonar_front_status(data['front_status'])
    if 'back_status' in data:
        update_sonar_back_status(data['back_status'])
    if 'distance' in data:
        update_sonar_distance(data['distance'])
    if 'latency_status' in data:
        update_latency_status(data['latency_status'])
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
