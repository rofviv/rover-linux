#!/bin/bash

source $PROJECT_ROOT/.venv/bin/activate

session_name="dashboard_session"
command="python $PROJECT_ROOT/src/dashboard/app.py"

screen -dmS "$session_name" bash -c "$command"