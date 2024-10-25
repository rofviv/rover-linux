#!/bin/bash

source $PROJECT_ROOT/.venv/bin/activate

session_name="latency_session"
command="python $PROJECT_ROOT/src/scripts/latency.py"

screen -dmS "$session_name" bash -c "$command"

