from rplidar import RPLidar
import time

lidar = RPLidar('/dev/ttyUSB0', 256000)

range_distance = 500
# range_angule = 50
# half_range_angule = range_angule / 2
# min_angle = 0.0
# max_angle = 359.9

info = lidar.get_info()
print(info)

print("Starting spinning .......\n")
time.sleep(5)
print("Scanning started\n")
print(f"Range distance = {range_distance}")

try:
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            if distance < range_distance:
            # Verifica si el ángulo está en el rango de 350 a 359 grados o de 0 a 20 grados
            # if (angle >= (max_angle - half_range_angule) or angle <= (min_angle + half_range_angule)) and distance < range_distance:
                print(f"Objeto detectado a {distance} mm en el ángulo {angle} grados")
                print("\n")

except KeyboardInterrupt:
    print('Stopping.')

finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


