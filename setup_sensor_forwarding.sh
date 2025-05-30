#!/bin/sh

###########################################################
# Install packages
###########################################################

# Install necessary dependencies for Bluetooth
sudo apt-get update
sudo apt-get install -y python3-pip libglib2.0-dev

# Install Python dependencies
# pip3 install bleak
# pip3 install paho.mqtt
# pip3 install requests

sudo apt install -y python3-bleak
sudo apt install -y python3-paho-mqtt
sudo apt install -y python3-requests
sudo apt install -y python3-signal

export PYTHONPATH=./src/python/

# python3 ./src/python/main.py


#########################################################
# Confirm that everything is OK
#########################################################
echo "[SETUP-BLUETOOTH-AND-FORWARDING: SUCCESS]"
