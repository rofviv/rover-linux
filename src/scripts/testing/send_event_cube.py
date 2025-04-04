import socketio
import time

print("SCRIPT TEST CUBE")

sio = socketio.Client()
sio.connect('http://localhost:5000')
armado_str = "ARMED"
safety_str = "SAFE"
mode = 'MANUAL'
lat = -17.863149928443632
lon = -63.186119067990506
alt = 0.0
battery_percentage = 0
roll = 0
pitch = 0
yaw = 190.0
rc_values = {
    'ch1': 1000,
    'ch2': 1000,
    'ch3': 1000,
    'ch4': 1000,
    'ch5': 1000,
    'ch6': 1000,
    'ch7': 1000,
    'ch8': 1000,
}

sio.emit('cube_data', {'armado_str': armado_str, 'safety_str': safety_str, 'mode': mode, 'lat': lat, 'lon': lon, 'alt': alt, 'battery_percentage': battery_percentage, 'roll': roll, 'pitch': pitch, 'yaw': yaw, 'rc_values': rc_values})
time.sleep(2)