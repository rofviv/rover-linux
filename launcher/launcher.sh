#!/bin/bash

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

echo "Laucher master starting..."

sleep 10

checkinternet() {
	if ! ping -c 1 www.google.com &> /dev/null
	then
		echo "No connection internet. Failed. Retry in 5 seconds"
		sleep 5
		checkinternet
	else
		# xdg-open "$MEET_LINK" &
		echo "Opening camera stream"
		bash "$PROJECT_ROOT/launcher/screen_camera.sh" &
		sleep 10

		echo "Opening mavproxy"
		bash "$PROJECT_ROOT/launcher/screen_mavproxy.sh" &
		sleep 10

		echo "Opening script latency"
		bash "$PROJECT_ROOT/launcher/screen_latency.sh" &
		sleep 10

		echo "Opening dashboard"
		bash "$PROJECT_ROOT/launcher/screen_dashboard.sh" &
		sleep 10

	fi
}

checkinternet
