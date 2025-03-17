#!/bin/bash

NONE='\033[00m'
RED='\033[01;31m'
GREEN='\033[01;32m'
YELLOW='\033[01;33m'
PURPLE='\033[01;35m'
CYAN='\033[01;36m'
WHITE='\033[01;37m'
BOLD='\033[1m'
UNDERLINE='\033[4m'

ENV_FILE="/home/dev/Projects/rover-linux/config/.env"

if [ -f "$ENV_FILE" ]; then
    export $(grep -Ev '^\s*#|^\s*$' "$ENV_FILE" | xargs -d '\n')
fi

echo -e "${BOLD}EnviromentFile:${NONE} $ENV_FILE"
echo ""
grep -Ev '^\s*#|^\s*$' "$ENV_FILE" | cut -d '=' -f 1 | while read -r var; do
    echo -e "${BOLD}$var:${NONE} ${!var}"
done

echo ""
echo -e "${CYAN}* To execute launcher. run:${NONE}"
echo "bash \$PROJECT_ROOT/launcher/launcher.sh"
echo ""
echo -e "${CYAN}* To verify the scripts. run:${NONE}"
echo "screen -ls"
echo ""
