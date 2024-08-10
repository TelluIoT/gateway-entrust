#!/bin/sh

###########################################################
# Install packages
###########################################################

# Install necessary dependencies for Bluetooth and Bleak
sudo apt-get install -y python3-pip libglib2.0-dev

# Install Python dependencies
pip3 install bleak

export PYTHONPATH=./src/python/bluetooth

python3 ./src/python/bluetooth/main.py


#########################################################
# Confirm that everything is OK
#########################################################
echo "[SETUP-BLUETOOTH: SUCCESS]"
