#!/bin/bash

sudo ip route add 192.168.18.0/24 dev wg0
sudo ip route add 10.13.13.0/24 dev wg0