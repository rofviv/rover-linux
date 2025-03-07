#!/bin/bash
export DISPLAY=:0
session_name="dashboard_session"

if screen -ls | grep -q "$session_name"; then
    echo "$session_name already exists! For quit run:"
    echo "screen -X -S $session_name quit"
    echo ""
    exit 0
fi

command="$PROJECT_ROOT/app/rover_relay"

> "$PROJECT_ROOT/logs/$session_name.log"
screen -L -Logfile "$PROJECT_ROOT/logs/$session_name.log" -dmS "$session_name" bash -c "$command"
sleep 1
screen -ls
