from flask import Flask, render_template, jsonify
import subprocess
import socket
import getpass
import time
import threading
import datetime
import os
import argparse

app = Flask(__name__)

# Variable global para almacenar la hora de inicio
START_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_launcher_dir():
    if hasattr(app, 'launcher_dir'):
        return app.launcher_dir
    return '../../launcher'

@app.route('/')
def index():
    username = getpass.getuser()
    return render_template('index.html', username=username, start_time=START_TIME)

@app.route('/get_screens')
def get_screens():
    try:
        # Ejecutar comando screen -ls para listar las screens
        result = subprocess.run(['screen', '-ls'], capture_output=True, text=True)
        screens = []
        
        # Procesar la salida para obtener las screens
        for line in result.stdout.split('\n'):
            if '\t' in line:  # Las líneas con screens tienen un tab
                screen_info = line.strip().split('\t')[0]
                screens.append(screen_info)
        
        return jsonify({'screens': screens})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/execute_screen/<screen_name>')
def execute_screen(screen_name):
    try:
        # Usar LAUNCHER_DIR para construir la ruta
        script_path = f'{get_launcher_dir()}/{screen_name}.sh'
        
        # Ejecutar el script bash
        result = subprocess.run(['bash', script_path], capture_output=True, text=True)
        
        return jsonify({
            'success': True,
            #'output': result.stdout,
            'output': f'{screen_name} executed',
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/kill_screen/<screen_name>')
def kill_screen(screen_name):
    try:
        # Ejecutar comando para matar la screen
        result = subprocess.run(['screen', '-X', '-S', screen_name, 'quit'], 
                              capture_output=True, 
                              text=True)
        
        return jsonify({
            'success': True,
            'message': f'Screen {screen_name} killed successfully',
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/get_screen_log/<screen_name>')
def get_screen_log(screen_name):
    try:
        # Obtener el contenido de la screen usando hardcopy
        log_file = f'/tmp/{screen_name}_log.txt'
        
        # Primero crear el hardcopy de la screen
        subprocess.run(['screen', '-S', screen_name, '-X', 'hardcopy', log_file])
        
        # Esperar un momento para asegurar que el archivo se ha creado
        time.sleep(0.5)
        
        # Leer el contenido del archivo
        try:
            with open(log_file, 'r') as f:
                content = f.read()
            # Limpiar el archivo temporal
            os.remove(log_file)
        except FileNotFoundError:
            content = "No logs available"
            
        return jsonify({
            'success': True,
            'log': content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


def run_launcher_script():
    time.sleep(3)
    try:
        # Usar LAUNCHER_DIR para construir la ruta
        script_path = f'{get_launcher_dir()}/launcher.sh'
        result = subprocess.run(['bash', script_path], capture_output=True, text=True)
        print(result)
    except Exception as e:
        print(f"Error executing launcher script: {str(e)}")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Path to launcher")
    parser.add_argument('--launcher-dir', default=get_launcher_dir(), help='Path to launcher')
    args = parser.parse_args()
    app.launcher_dir = args.launcher_dir
    print(f"Parameters:\n  --launcher-dir={get_launcher_dir()}\n")

    launcher_thread = threading.Thread(target=run_launcher_script)
    launcher_thread.daemon = True
    launcher_thread.start()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
