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
sed -i 's/GATEWAYID/10.0.0.9/g' /etc/tellugw/prometheus.yml

###########################################################
# Create persistent data directory for Prometheus
###########################################################
mkdir -p /var/prometheus

echo "[ALL: SUCCESS]"
