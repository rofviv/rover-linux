from flask import Flask, render_template
from flask_socketio import SocketIO
import serial
import time
import threading

# Configuración del servidor Flask + SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

max_speed = 100

# Configuración del puerto serial
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Espera a que el Arduino reinicie

# Variables de estado
last_command_time = 0
command_lock = threading.Lock()
current_motion = None
COMMAND_TIMEOUT = 0.5  # segundos

# Función para enviar comandos al Arduino
def enviar_comando(velocidad):
    comando = f"M{velocidad}\n"
    arduino.write(comando.encode())
    print(f"[SERIAL →] {comando.strip()}")

# Hilo que monitorea el puerto serial constantemente
def monitor_serial():
    while True:
        if arduino.in_waiting:
            linea = arduino.readline().decode(errors='ignore').strip()
            if linea:
                print(f"[SERIAL ←] {linea}")
                socketio.emit('arduino_output', {'linea': linea})

# Hilo de seguridad que detiene los motores si no hay comandos recientes
def watchdog_loop():
    global last_command_time, current_motion
    while True:
        time.sleep(0.1)
        with command_lock:
            if current_motion is not None and (time.time() - last_command_time > COMMAND_TIMEOUT):
                enviar_comando(0)
                current_motion = None
                print("[INFO] Motores detenidos por inactividad")

# Iniciar hilos en segundo plano
threading.Thread(target=monitor_serial, daemon=True).start()
threading.Thread(target=watchdog_loop, daemon=True).start()

# Evento cuando el cliente presiona una tecla
@socketio.on('tecla')
def on_tecla(data):
    global last_command_time, current_motion
    key = data.get('key')
    
    if key == 'W':  # Avanzar
        comando = f"M{max_speed}\n"  # Ambos motores a velocidad máxima
    elif key == 'A':  # Girar izquierda
        comando = f"A0B{max_speed}\n"  # Motor A detenido, B a máxima velocidad
    elif key == 'D':  # Girar derecha
        comando = f"B0A{max_speed}\n"  # Motor A a máxima velocidad, B detenido

    with command_lock:
        last_command_time = time.time()
        if current_motion != comando:
            arduino.write(comando.encode())
            print(f"[SERIAL →] {comando.strip()}")
            current_motion = comando

@app.route('/')
def index():
    return render_template('index.html')  # busca en la carpeta "templates"

# Ejecutar servidor
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
