#!/bin/sh

###########################################################
# Install packages
###########################################################

# Install necessary dependencies for Bluetooth and Bleak
sudo apt-get install -y python3-pip libglib2.0-dev

# Install Bleak via pip
pip3 install bleak


#########################################################
# Confirm that everything is OK
#########################################################
echo "[SETUP-BLUETOOTH: SUCCESS]"
