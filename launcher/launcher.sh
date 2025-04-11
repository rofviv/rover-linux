#!/bin/bash

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

echo "Laucher master starting..."

sleep 5

echo "Starting OBS virtual cam"
bash "$PROJECT_ROOT/launcher/screen_obs.sh" &

sleep 5

checkinternet() {
	if ! ping -c 1 www.google.com &> /dev/null
	then
		echo "No connection internet. Failed. Retry in 5 seconds"
		sleep 5
		checkinternet
	else
		echo "Opening mavproxy"
		bash "$PROJECT_ROOT/launcher/screen_mavproxy.sh" &
		sleep 10

		echo "Opening script find esp ip"
		bash "$PROJECT_ROOT/launcher/find_esp_ip.sh" &
		sleep 10


		# TODO: DEPRECATED
		# echo "Opening script sensor server"
		# bash "$PROJECT_ROOT/launcher/screen_sensor_server.sh" &
		# sleep 10

		echo "Opening script rover api"
		bash "$PROJECT_ROOT/launcher/screen_rover_api.sh" &
		sleep 10

		echo "Opening script latency"
		bash "$PROJECT_ROOT/launcher/screen_latency.sh" &
		sleep 10

		# echo "Opening script lidar"
		# bash "$PROJECT_ROOT/launcher/screen_lidar.sh" &
		# sleep 10

		echo "Opening script sonar"
		bash "$PROJECT_ROOT/launcher/screen_sonar.sh" &
		sleep 10

		echo "Opening script nextion"
		bash "$PROJECT_ROOT/launcher/screen_nextion.sh" &
		sleep 10

		echo "Adding routes to launcher rover"
		bash "$PROJECT_ROOT/launcher/add_ip_route.sh" &
		sleep 10

		echo "Opening script CUBE listening"
		bash "$PROJECT_ROOT/launcher/screen_cube.sh" &
		sleep 10

		# echo "Opening App Dashboard"
		# bash "$PROJECT_ROOT/launcher/screen_dashboard.sh" &
		# sleep 10

		echo "Opening meet"
		bash "$PROJECT_ROOT/launcher/screen_meet.sh" &
		sleep 10

		echo "Exit"
	fi
}

checkinternet
