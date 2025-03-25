from pymavlink import mavutil
import math

# Conectar al CUBE (ajusta el puerto si es necesario)
master = mavutil.mavlink_connection('udp:192.168.0.21:14551')

# Esperar el primer latido del CUBE
master.wait_heartbeat()
print("✅ Conectado al CUBE")

while True:
    # Obtener estado del dron
    msg_heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)
    if msg_heartbeat:
        # Verificar si está armado
        is_armed = msg_heartbeat.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
        armado_str = "ARMADO" if is_armed else "DESARMADO"

        # Verificar si está en modo SAFETY
        is_safety = not (msg_heartbeat.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
        safety_str = "SAFETY ACTIVADO" if is_safety else "SAFETY DESACTIVADO"

        # Obtener modo de vuelo
        mode = master.flightmode  # pymavlink traduce el modo automáticamente
        print(f"🛩️ Estado -> {armado_str}, {safety_str}, Modo: {mode}")

    # Recibir datos del GPS
    msg_gps = master.recv_match(type='GPS_RAW_INT', blocking=True)
    if msg_gps:
        lat = msg_gps.lat / 1e7
        lon = msg_gps.lon / 1e7
        alt = msg_gps.alt / 1000
        print(f"📡 GPS -> Lat: {lat}, Lon: {lon}, Alt: {alt}m")

    # Recibir porcentaje de batería
    msg_battery = master.recv_match(type='SYS_STATUS', blocking=True)
    if msg_battery:
        battery_percentage = msg_battery.battery_remaining
        print(f"🔋 Batería -> {battery_percentage}%")

    # Recibir orientación
    msg_attitude = master.recv_match(type='ATTITUDE', blocking=True)
    if msg_attitude:
        roll = math.degrees(msg_attitude.roll)
        pitch = math.degrees(msg_attitude.pitch)
        yaw = math.degrees(msg_attitude.yaw)
        print(f"🧭 Orientación -> Roll: {roll:.2f}°, Pitch: {pitch:.2f}°, Yaw: {yaw:.2f}°")

    # Recibir valores de los canales RC
    msg_rc = master.recv_match(type='RC_CHANNELS', blocking=True)
    if msg_rc:
        rc_values = [msg_rc.chan1_raw, msg_rc.chan2_raw, msg_rc.chan3_raw, msg_rc.chan4_raw,
                     msg_rc.chan5_raw, msg_rc.chan6_raw, msg_rc.chan7_raw, msg_rc.chan8_raw]
        print(f"🎛️ RC Channels -> {rc_values}")

    print("---------------------------------------------------")
