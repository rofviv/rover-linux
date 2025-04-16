from rplidar import RPLidar
import time
import socketio

lidar = RPLidar('/dev/ttyUSB0', 256000)
sio = socketio.Client()
sio.connect('http://localhost:5000')
# sio.wait()

range_distance = 500
range_angle = 45

info = lidar.get_info()
print(info)

print("Starting spinning .......\n")
time.sleep(5)
print("Scanning started\n")
print(f"Range distance = {range_distance}")

try:
    for scan in lidar.iter_scans():
        half_range_angle = range_angle / 2
        for (_, angle, distance) in scan:
            if (angle >= (360 - half_range_angle) or angle <= half_range_angle) and distance < range_distance:
                print(f"Objeto detectado a {distance} mm en el ángulo {angle} grados")
                print("\n")
                sio.emit('sensor_data', {'sensor': 'lidar', 'distance': distance, 'angle': angle})


except KeyboardInterrupt:
    print('Stopping.')

finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


