#!/bin/bash

source $PROJECT_ROOT/.venv/bin/activate

mavproxy_command="mavproxy.py --master=$PORT_CUBE --out=udp:$IP_LOCAL_MAVPROXY:14551 --out=udp:$IP_REMOTE_MAVPROXY:14550 --logfile=$PROJECT_ROOT/logs/mav.tlog"

screen -dmS "$SCREEN_SESSION_NAME" bash -c "$mavproxy_command"

