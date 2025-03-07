#!/bin/bash
export DISPLAY=:0

# IMPORTANT: CHANGE USER TO YOURS
source /home/rd2-0/Projects/rover-linux/config/config.sh
session_name="obs_session"

if screen -ls | grep -q "$session_name"; then
    echo "$session_name already exists! For quit run:"
    echo "screen -X -S $session_name quit"
    echo ""
    exit 0
fi

rm -r $HOME/.config/obs-studio/safe_mode
sudo /sbin/modprobe v4l2loopback
command="obs --startvirtualcam"

# screen -dmS "$session_name" bash -c "$command 2>&1 | tee $PROJECT_ROOT/logs/$session_name.log"
> "$PROJECT_ROOT/logs/$session_name.log"
screen -L -Logfile "$PROJECT_ROOT/logs/$session_name.log" -dmS "$session_name" bash -c "$command"
sleep 1
screen -ls