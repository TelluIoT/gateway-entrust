# Setup

## 0. Prepare a Raspberry Pi board:

1. Install the Raspberry Pi Imager on your computer: https://www.raspberrypi.com/software/

2. Using a SD-card burner tool, burn the "Raspberry Pi OS 64-bit" image (the default OS) onto the SD-card of the Raspberry Pi. In the wizard, you can prepare network access and enable SSH so it will be reachable on the local network on startup.

## 1.SSH into your RPi (on local network) and install Git, clone the repository and navigate into it

If you know the MAC address of the RPi, you can scan the network and determine its IP-address. If not, you can access the pi directly and get it from the terminal with `hostname -I`

`sudo apt-get update && sudo apt-get install -y git`

`git clone https://github.com/TelluIoT/gateway-entrust.git`

`cd gateway-entrust`

## 2. [Optional] Install zerotier to enable remote access

If the gateway is setup with remote access, it needs to be enabled in the zerotier admin together with username and password of the device. Further steps can then be done either remotely or locally

Take the ZeroTier Network ID that the gateway should be added to and pass to the deployment script

`bash ./zerotier_deploy.sh [ZeroTier network ID]`

## 3. and run the command to install Docker:

`curl -sSL https://get.docker.com | sh`

## 4. Run the docker setup script to copy files and install Docker-Compose:

`sudo sh install_docker.sh`

## 5. Download and run several Docker containers defined in docker-compose.yml at once:

`sudo docker compose up`

---
