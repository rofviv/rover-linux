import socketio
import time

print("SCRIPT TEST CUBE")

sio = socketio.Client()
sio.connect('http://localhost:5000')

sensor = 'sonar-2'
distance = 0

sio.emit('sensor_data', {'sensor': sensor, 'distance': distance})
time.sleep(2)