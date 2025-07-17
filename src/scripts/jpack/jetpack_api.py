from flask import Flask, render_template
from flask_socketio import SocketIO
import serial
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

default_speed = 80
default_factorA = 1.00
default_factorB = 1.00

# CHANGE DEVICE PORT AND IP LOCAL VPN WIREGUARD
port_serial = "/dev/ttyACM0"
port_serial_actuators = "/dev/ttyUSB1"
ip_local = "127.0.0.1"

# FALSE IS Development MODE. TRUE IS Production MODE.
is_production = True
is_production_actuators = True

if is_production:
    arduino = serial.Serial(port_serial, 9600, timeout=1)
    time.sleep(2)


if is_production_actuators:
    arduino_actuators = serial.Serial(port_serial_actuators, 115200, timeout=1)
    time.sleep(2)

last_command_time = 0
command_lock = threading.Lock()
current_motion = None
COMMAND_TIMEOUT = 0.5  # segundos


def enviar_comando(velocidad_izq, velocidad_der):
    comando = f"M{velocidad_izq}-{factorA:.2f},{velocidad_der}-{factorB:.2f}\n"
    if is_production:
        arduino.write(comando.encode())


def monitor_serial():
    while True:
        if is_production:
            if arduino.in_waiting:
                linea = arduino.readline().decode(errors='ignore').strip()
                if linea:
                    socketio.emit('arduino_output', {'linea': linea})

        if is_production_actuators:
            if arduino_actuators.in_waiting:
                linea = arduino_actuators.readline().decode(errors='ignore').strip()
                if linea:
                    socketio.emit('arduino_output_actuators', {'linea': linea})

def watchdog_loop():
    global last_command_time, current_motion
    while True:
        time.sleep(0.1)
        with command_lock:
            if current_motion is not None and (time.time() - last_command_time > COMMAND_TIMEOUT):
                enviar_comando(0, 0)
                current_motion = None
                print("[INFO] Motores detenidos por inactividad")


threading.Thread(target=monitor_serial, daemon=True).start()
threading.Thread(target=watchdog_loop, daemon=True).start()


@socketio.on('movimiento')
def on_movimiento(data):
    global last_command_time, current_motion, factorA, factorB

    keys = data.get('keys', [])
    speedA = int(data.get('speedA', default_speed))
    speedB = int(data.get('speedB', default_speed))
    factorA = default_factorA
    factorB = default_factorB

    velocidad_izq = speedA if 'W' in keys else 0
    velocidad_der = speedB if 'E' in keys else 0

    nuevo_motion = (velocidad_izq, velocidad_der, factorA, factorB)

    with command_lock:
        last_command_time = time.time()
        if current_motion != nuevo_motion:
            enviar_comando(velocidad_izq, velocidad_der)
            current_motion = nuevo_motion

@socketio.on('actuators')
def on_actuators(data):
    if data.get('key') == 'f':
        comando = f"f\n".encode('utf-8')
    elif data.get('key') == 'r':
        comando = f"r\n".encode('utf-8')
    elif data.get('key') == 's':
        comando = f"s\n".encode('utf-8')
    elif data.get('key') == 'dr' and data.get('value') == 'on':
        comando = f"dr on\n".encode('utf-8')
    elif data.get('key') == 'dr' and data.get('value') == 'off':
        comando = f"dr off\n".encode('utf-8')
    elif data.get('key') == 'iz' and data.get('value') == 'on':
        comando = f"iz on\n".encode('utf-8')
    elif data.get('key') == 'iz' and data.get('value') == 'off':
        comando = f"iz off\n".encode('utf-8')
    elif data.get('key') == 'rev1' and data.get('value') == 'on':
        comando = f"rev1 on\n".encode('utf-8')
    elif data.get('key') == 'rev1' and data.get('value') == 'off':
        comando = f"rev1 off\n".encode('utf-8')
    elif data.get('key') == 'rev2' and data.get('value') == 'on':
        comando = f"rev2 on\n".encode('utf-8')
    elif data.get('key') == 'rev2' and data.get('value') == 'off':
        comando = f"rev2 off\n".encode('utf-8')
    elif data.get('key') == 'charge' and data.get('value') == 'on':
        comando = f"charge on\n".encode('utf-8')
    elif data.get('key') == 'charge' and data.get('value') == 'off':
        comando = f"charge off\n".encode('utf-8')
    else:
        comando = f"{data.get('key')} {data.get('value')}\n".encode('utf-8')
        
    arduino_actuators.write(comando)

@app.route('/')
def index():
    return render_template('index.html', ip_local=ip_local)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
