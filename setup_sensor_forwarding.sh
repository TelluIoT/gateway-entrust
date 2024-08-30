#!/bin/sh

###########################################################
# Install packages
###########################################################

# Install necessary dependencies for Bluetooth
sudo apt-get update
sudo apt-get install -y python3-pip libglib2.0-dev

# Install Python dependencies
pip3 install bleak
pip3 install paho.mqtt
pip3 install requests

export PYTHONPATH=./src/python/

# python3 ./src/python/main.py


#########################################################
# Confirm that everything is OK
#########################################################
echo "[SETUP-BLUETOOTH-AND-FORWARDING: SUCCESS]"
