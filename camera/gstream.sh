#!/bin/bash

OUTPUT_PORT="8080"

gst-launch-1.0 v4l2src device=$PORT_CAMERA ! \
    videoconvert ! video/x-raw,width=640,height=480 ! \
    vp8enc deadline=1 ! \
    rtpvp8pay ! \
    udpsink host=$IP_REMOTE_MAVPROXY port=$OUTPUT_PORT


