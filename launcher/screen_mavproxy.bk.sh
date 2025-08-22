#!/bin/bash

if screen -ls | grep -q "$SCREEN_SESSION_NAME"; then
    echo "$SCREEN_SESSION_NAME already exists! For quit run:"
    echo "screen -X -S $SCREEN_SESSION_NAME quit"
    echo ""
    exit 0
fi

source $PROJECT_ROOT/.venv/bin/activate
command="mavproxy.py --master=/dev/ttyACM1 --out=udp:$IP_LOCAL_MAVPROXY:14551 --out=udp:$IP_REMOTE_MAVPROXY:14550 --logfile=$PROJECT_ROOT/logs/mav.tlog"

# screen -dmS "$SCREEN_SESSION_NAME" bash -c "$command"
> "$PROJECT_ROOT/logs/$SCREEN_SESSION_NAME.log"
screen -L -Logfile "$PROJECT_ROOT/logs/$SCREEN_SESSION_NAME.log" -dmS "$SCREEN_SESSION_NAME" bash -c "$command"
sleep 1
screen -ls