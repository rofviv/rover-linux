#!/bin/bash

# Buscar el primer dispositivo disponible /dev/ttyACM*
DEVICE=$(ls -1 /dev/ttyACM* 2>/dev/null | head -n 1)

if [ -z "$DEVICE" ]; then
    echo "❌ No se encontró ningún dispositivo /dev/ttyACM* conectado."
    exit 1
fi

echo "✅ Usando dispositivo: $DEVICE"

if screen -ls | grep -q "$SCREEN_SESSION_NAME"; then
    echo "$SCREEN_SESSION_NAME already exists! For quit run:"
    echo "screen -X -S $SCREEN_SESSION_NAME quit"
    echo ""
    exit 0
fi

source "$PROJECT_ROOT/.venv/bin/activate"
command="mavproxy.py --master=$DEVICE --out=udp:$IP_LOCAL_MAVPROXY:14551 --out=udp:$IP_REMOTE_MAVPROXY:14550 --logfile=$PROJECT_ROOT/logs/mav.tlog"

# Log limpio
> "$PROJECT_ROOT/logs/$SCREEN_SESSION_NAME.log"

# Lanzar en screen con logging
screen -L -Logfile "$PROJECT_ROOT/logs/$SCREEN_SESSION_NAME.log" -dmS "$SCREEN_SESSION_NAME" bash -c "$command"

sleep 1
screen -ls
