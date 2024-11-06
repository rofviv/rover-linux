#!/bin/bash

OUTPUT_PORT="8080"
#DEVICE=$PORT_CAMERA
DEVICE="/dev/video0"

gst-launch-1.0 v4l2src device=$DEVICE ! \
    videoconvert ! video/x-raw,width=640,height=480 ! \
    vp8enc deadline=1 ! \
    rtpvp8pay ! \
    udpsink host=$IP_REMOTE_MAVPROXY port=$OUTPUT_PORT

#gst-launch-1.0 v4l2src device=$DEVICE io-mode=2 ! \
#    video/x-raw,format=YUY2 ! \
#    videoconvert ! \
#    vp8enc deadline=1 cpu-used=4 ! \
#    rtpvp8pay ! \
#    udpsink host=$IP_REMOTE_MAVPROXY port=$OUTPUT_PORT

