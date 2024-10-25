#!/bin/bash

session_name="camera_session"
command="bash $PROJECT_ROOT/camera/gstream.sh"

screen -dmS "$session_name" bash -c "$command"
