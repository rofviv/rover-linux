#!/bin/bash

OUTPUT_PORT2="8081"
DEVICE=$PORT_CAMERA_2    #"/dev/video4"

gst-launch-1.0 v4l2src device=$DEVICE ! \
    videoconvert ! video/x-raw,width=640,height=480 ! \
    vp8enc deadline=1 ! \
    rtpvp8pay ! \
    udpsink host=$IP_REMOTE_MAVPROXY port=$OUTPUT_PORT2
