#!/bin/bash

OUTPUT_PORT="8080"

gst-launch-1.0 udpsrc port=$OUTPUT_PORT ! \
    application/x-rtp, encoding-name=VP8, payload=96 ! \
    rtpvp8depay ! \
    vp8dec ! \
    videoconvert ! \
    autovideosink
