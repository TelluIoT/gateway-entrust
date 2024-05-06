# Setup

## 0. Prepare a Raspberry Pi board: Deploy Raspbian OS, setup SSH and network connection according to Franck's instructions below

## 1. SSH into your RPi and run the command to install Docker:

`curl -sSL https://get.docker.com | sh`

## 2. Install Git, clone the repository and navigate into it

`sudo apt-get update && sudo apt-get install -y git`

`git clone https://github.com/TelluIoT/gateway-entrust.git`

`cd gateway-entrust`

## 3. [Optional] Install zerotier to enable remote access
chmod -x zerotier_install.sh
sudo zerotier_deploy.sh

If the gateway is setup with remote access, it needs to be enabled in the zerotier admin together with username and password of the device. Further steps can then be done remotely (or locally if preferred)

## 4. Run the docker setup script to copy files and install Docker-Compose:
`sudo sh script.sh`

## 5. Download and run several Docker containers defined in docker-compose.yml at once:

`sudo docker-compose up`

---
