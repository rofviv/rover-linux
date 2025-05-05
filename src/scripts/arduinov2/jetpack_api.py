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

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Espera a que el Arduino reinicie


last_command_time = 0
command_lock = threading.Lock()
current_motion = None
COMMAND_TIMEOUT = 0.5  # segundos

def enviar_comando(velocidad_izq, velocidad_der):
    comando = f"M{velocidad_izq}-{factorA:.2f},{velocidad_der}-{factorB:.2f}\n"
    arduino.write(comando.encode())


def monitor_serial():
    while True:
        if arduino.in_waiting:
            linea = arduino.readline().decode(errors='ignore').strip()
            if linea:
                print(f"[SERIAL ←] {linea}")
                socketio.emit('arduino_output', {'linea': linea})


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
    factorA = float(data.get('factorA', default_factorA))
    factorB = float(data.get('factorB', default_factorB))

    velocidad_izq = speedA if 'W' in keys else 0
    velocidad_der = speedB if 'E' in keys else 0

    nuevo_motion = (velocidad_izq, velocidad_der, factorA, factorB)

    with command_lock:
        last_command_time = time.time()
        if current_motion != nuevo_motion:
            enviar_comando(velocidad_izq, velocidad_der)
            current_motion = nuevo_motion

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
