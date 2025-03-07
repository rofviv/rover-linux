#!/bin/bash
# Change to the path of the project
source /home/rd2-1/Projects/rover-linux/config/config.sh

LAUNCHER_DIR=${1:-"launcher"}

echo "Parameter: $LAUNCHER_DIR"

NONE='\033[00m'
RED='\033[01;31m'
GREEN='\033[01;32m'

session_name="panel_session"

if screen -ls | grep -q "$session_name"; then
    echo -e "${RED}$session_name already exists! For quit run:${NONE}"
    echo "screen -X -S $session_name quit"
    echo ""
    exit 0
fi

source $PROJECT_ROOT/.venv/bin/activate

command="$PYTHON $PROJECT_ROOT/src/panel/app.py --launcher-dir=$LAUNCHER_DIR"

screen -dmS "$session_name" bash -c "$command 2>&1 | tee $PROJECT_ROOT/logs/$session_name.log"

echo -e "${GREEN}Panel running... [OK]${NONE}"
echo "http://$IP_LOCAL_MAVPROXY:5000"
echo ""
