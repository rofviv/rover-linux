#!/bin/bash
source $PROJECT_ROOT/.venv/bin/activate

"$PYTHON" "$PROJECT_ROOT/src/scripts/find_esp_ip.py" > "$PROJECT_ROOT/logs/find_esp_ip.log" 2>&1