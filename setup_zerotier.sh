#!/bin/sh

# toggle fail fast
# set -e

###########################################################
# Verify network id parameter was received
###########################################################
if [ $# -ne 1 ]; then
	echo "Missing ZeroTier Network ID as input argument, setup cancelled"
	exit 1;
fi

input_network_id="$1"

###########################################################
# Install zerotier
###########################################################
bash ./src/zerotier/zerotier_install.sh

###########################################################
# Connect to zerotier network
###########################################################
bash ./src/zerotier/zerotier_connect.sh $input_network_id

#########################################################
# Confirm that everything is OK
#########################################################
echo "[ZEROTIER-DEPLOY: SUCCESS]"
