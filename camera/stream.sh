#!/bin/bash

OUTPUT_PORT="8082"

ffmpeg -f v4l2 -video_size 640x480 -i /dev/video4 -c:v mpeg1video -preset ultrafast -tune zerolatency -r 30 -b:v 500k -fflags nobuffer -flush_packets 1 -f mpegts "udp://$IP_REMOTE_MAVPROXY:$OUTPUT_PORT?pkt_size=1200&ttl=16&buffer_size=500000&max_delay=0"
#ffmpeg -f v4l2 -video_size 640x480 -i $PORT_CAMERA -c:v libx264 -preset ultrafast -tune zerolatency -r 15 -fflags nobuffer -flush_packets 1 -f mpegts "udp://$IP_REMOTE_MAVPROXY:$OUTPUT_PORT?pkt_size=512&ttl=16&buffer_size=200000&max_delay=0"


