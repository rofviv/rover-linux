### ROVER LINUX

### Skills
- Ubuntu
- Python
- Bash
- Wireguard
- Docker

#### Prepare SO and Project
- IMPORTANT: Read the documentation -> instalation/ubuntu22.04.md

- Create Environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Launch scripts in one:
```bash
bash $PROJECT_ROOT/launcher/launcher.sh
```

- Check proccess
```bash
screen -ls
```

#### Scripts
- Mavproxy (Cube)
- Lidar
- Arduino (Sonar ultrasonic)
- Nextion
- OBS cameras
- App dashboard
- Relay connection (From app dashboard)

#### PROJECT STRUCTURE
- app
Aplicacion flutter compilada para linux, encargada de controlar los estados del robot. Se ejecuta ./rover_relay desde la consola

- assets
Images, files, etc...

- camera
Streaming camera replace obs and meet. Only used in case OBS not working. Normally used only for raspberry. For Ubuntu OBS and meet is working successfuly
Read README.md for more information

- config
- .env
Variable globales usadas en todo el proyecto
- config
Encargado de leer todas las variables del archivo .env y publicarlos en todo el sistema, Incluye informacion de variables configuradas y comandos de inicio y revision de scripts. Este archivo debe estar en el .bashrc del sistema para ejectuarse siempre

- instalation
Archivos de instrucciones para configurar el sistema operativo. Disponible para Ubuntu 22.04 y Raspberry pi

- launcher
Son todos los scripts bash encargados de levantar cada proceso que necesita el proyecto para funcionar.
- launcher.sh
Ejecuta todos los scripts bash en uno solo. Este se debe ejecutar cada vez que se inicie el sistema y levantar todos los procesos en un solo archivo.
- meet.sh
Ejecuta el navegador con una url meet configurada
- screen_camera.sh
Ejecuta el streaming camera/gstream.sh Solo se usa en sistemas donde no funciona OBS, normalmente Raspberry pi. En ubuntu no es necesario ejecutarlo
- screen_dashboard.sh
Ejecuta el software del robot, la app que se encarga de comunicarse con los relays y cambias algunos estados
- screen_latency.sh
Ejecuta el script de latencia para verificar el estado de la senal, si sobrepasa el limite, ejecutara comandos mavlink
- screen_lidar.sh
Script del sensor lidar, si detecta objetos manda senales al sensor server.
- screen_mavproxy.sh
Encargado de comunicarse con MavProxy para comandos del CUBE
- screen_obs.sh 
Abre el programa OBS
- screen_sensor_server.sh
Es el encargado de escuchar los eventos de los sensores lidar y sonar, y envia comando mavlink
- screen_sonar.sh
Sensor sonar ultrasonico, si detecta objetos manda senales al sensor server.

- logs
Logs del mavproxy

- src
Codigo fuente del proyecto
- panel
Sistema version web para controlar los estados de los procesos screen del sistema
- scripts
Todos los scripts escritos en python para hacer funcionar los sensores
- testing
Script para testear cada componente independiente

- status
Archivos .txt que tienen valores que controlan el estado del robot. Estos archivos son leidos desde los scripts

- wireguard
Es la VPN, la configuracion servidor y los clientes
- config
Contiene clientes peer, revisar cual esta disponible, tener duplicados puede causar conflictos

- requirements.txt
Librerias python necesarios para el proyecto. Se debe tener un entorno virtual activado .venv