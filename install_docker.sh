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
# Install Docker Compose, based on https://docs.docker.com/engine/install/raspberry-pi-os/#install-using-the-repository
##########################################################
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/raspbian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Set up Docker's APT repository:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/raspbian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

#########################################################
# Confirm that everything is OK
#########################################################
sudo docker run hello-world
echo "[ALL: SUCCESS]"
