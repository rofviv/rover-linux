Scripts for camera streaming
emitter: linux
file: gstream.sh
receiver: windows / linux
file: client_gstream.sh

INSTALLATION
LINUX - EMITTER
1.- install gstreamer:
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav

WINDOWS - RECEIVER
1.- install gstreamer:
https://gstreamer.freedesktop.org/download/#windows
2.- add bin path to environment variables:
C:\gstreamer\1.0\x86_64\bin
3.- execute in terminal:
gst-launch-1.0 udpsrc port=8080 caps="application/x-rtp,media=video,clock-rate=90000,encoding-name=VP8,payload=96" ! rtpvp8depay ! vp8dec ! videoconvert ! autovideosink