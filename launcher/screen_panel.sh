#!/bin/bash
session_name="panel_session"

if screen -ls | grep -q "$session_name"; then
    echo "$session_name already exists! For quit run:"
    echo "screen -X -S $session_name quit"
    echo ""
    exit 0
fi

source $PROJECT_ROOT/.venv/bin/activate
command="$PYTHON $PROJECT_ROOT/src/panel/app.py"

> "$PROJECT_ROOT/logs/$session_name.log"
screen -L -Logfile "$PROJECT_ROOT/logs/$session_name.log" -dmS "$session_name" bash -c "$command"
sleep 1
screen -ls