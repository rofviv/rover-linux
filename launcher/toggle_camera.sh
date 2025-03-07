#!/bin/bash

front_session="front_camera_session"
back_session="back_camera_session"

if screen -ls | grep "$front_session"; then
    screen -S "$front_session" -X stuff $'\003'
    bash "$PROJECT_ROOT/launcher/screen_back_camera.sh"
else
    if screen -ls | grep "$back_session"; then
        screen -S "$back_session" -X stuff $'\003'
        bash "$PROJECT_ROOT/launcher/screen_front_camera.sh"
    else
        bash "$PROJECT_ROOT/launcher/screen_front_camera.sh"
    fi
fi
