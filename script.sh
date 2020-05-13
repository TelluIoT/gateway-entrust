#!/bin/sh

set -e

###########################################################
# Create a destination folder
###########################################################
mkdir -p /etc/tellugw

###########################################################
# Take a copy of Prometheus config
###########################################################
cp ansible/public-files/prometheus.yml /etc/tellugw
# cp -r ansible/public-files/prometheus.yml /etc/tellugw

###########################################################
# Replace the gateway ID
###########################################################
sed -i 's/GATEWAYID/enact-gateway/g' /etc/tellugw/prometheus.yml

###########################################################
# Create persistent data directory for Prometheus
###########################################################
mkdir -p /var/prometheus

##########################################################
# Install Docker-Compose
##########################################################
apt-get install -y libffi-dev libssl-dev python3 python3-pip
apt-get remove python-configparser
pip3 install docker-compose

#########################################################
# Confirm that everything is OK
#########################################################
echo "[ALL: SUCCESS]"
