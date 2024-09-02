#!/bin/sh

# toggle fail fast
# set -e

###########################################################
# Install zerotier
###########################################################
curl https://raw.githubusercontent.com/zerotier/ZeroTierOne/master/doc/contact%40zerotier.com.gpg | gpg --dearmor | sudo tee /usr/share/keyrings/zerotierone-archive-keyring.gpg >/dev/null

RELEASE=$(lsb_release -cs)

echo "deb [signed-by=/usr/share/keyrings/zerotierone-archive-keyring.gpg] http://download.zerotier.com/debian/$RELEASE $RELEASE main" | sudo tee /etc/apt/sources.list.d/zerotier.list

sudo apt update

sudo apt install -y zerotier-one

#########################################################
# Confirm that everything is OK
#########################################################
echo "[ZEROTIER_INSTALL: SUCCESS]"
