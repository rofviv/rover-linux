from pymavlink import mavutil
import math
import os
import socketio
import time


print("SCRIPT CUBE")

sio = socketio.Client()

def main():
    print("Esperando heartbeat...")
    master.wait_heartbeat()
    print("✅ Conectado al CUBE")

    while True:
        msg_heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)
        if msg_heartbeat:
            is_armed = msg_heartbeat.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
            armado_str = "ARMED" if is_armed else "DISARMED"

            is_safety = not (msg_heartbeat.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
            safety_str = "SAFETY ACTIVADO" if is_safety else "SAFETY DESACTIVADO"

            mode = master.flightmode
            print(f"🛩️ Estado -> {armado_str}, {safety_str}, Modo: {mode}")


        msg_gps = master.recv_match(type='GPS_RAW_INT', blocking=True)
        if msg_gps:
            lat = msg_gps.lat / 1e7
            lon = msg_gps.lon / 1e7
            alt = msg_gps.alt / 1000
            print(f"📡 GPS -> Lat: {lat}, Lon: {lon}, Alt: {alt}m")


        msg_battery = master.recv_match(type='SYS_STATUS', blocking=True)
        if msg_battery:
            battery_percentage = msg_battery.battery_remaining
            print(f"🔋 Batería -> {battery_percentage}%")


        msg_attitude = master.recv_match(type='ATTITUDE', blocking=True)
        if msg_attitude:
            roll = math.degrees(msg_attitude.roll)
            pitch = math.degrees(msg_attitude.pitch)
            yaw = math.degrees(msg_attitude.yaw)
            print(f"🧭 Orientación -> Roll: {roll:.2f}°, Pitch: {pitch:.2f}°, Yaw: {yaw:.2f}°")


        msg_rc = master.recv_match(type='RC_CHANNELS', blocking=True)
        if msg_rc:
            rc_values = {
                'ch1': msg_rc.chan1_raw,
                'ch2': msg_rc.chan2_raw,
                'ch3': msg_rc.chan3_raw,
                'ch4': msg_rc.chan4_raw,
                'ch5': msg_rc.chan5_raw,
                'ch6': msg_rc.chan6_raw,
                'ch7': msg_rc.chan7_raw,
                'ch8': msg_rc.chan8_raw
            }
            print(f"🎛️ RC Channels -> {rc_values}")

        print("---------------------------------------------------")
        sio.emit('cube_data', {'armado_str': armado_str, 'safety_str': safety_str, 'mode': mode, 'lat': lat, 'lon': lon, 'alt': alt, 'battery_percentage': battery_percentage, 'roll': roll, 'pitch': pitch, 'yaw': yaw, 'rc_values': rc_values})
        time.sleep(1)

@sio.event
def connect():
    print('Conexión establecida con el servidor Socket.IO')
    main()

@sio.event
def disconnect():
    print('Desconectado del servidor Socket.IO')

if __name__ == "__main__":
    # ip_remote_mavproxy = os.getenv('IP_LOCAL_MAVPROXY', '10.13.13.1')
    ip_remote_mavproxy = '192.168.0.21'
    master = mavutil.mavlink_connection(f'udp:{ip_remote_mavproxy}:14551')

    while True:
        try:
            print("Intentando conectar al servidor Socket.IO...")
            sio.connect('http://localhost:5000')
            sio.wait()
            break
        except socketio.exceptions.ConnectionError:
            print("No se pudo conectar al servidor. Reintentando en 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Programa detenido por el usuario")
            break
