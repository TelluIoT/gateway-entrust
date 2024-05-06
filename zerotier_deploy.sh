#!/bin/sh

# toggle fail fast
# set -e


###########################################################
# Make the script executable
###########################################################
chmod +x "$0"


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
chmod +x zerotier_install.sh
./zerotier_install.sh

###########################################################
# Connect to zerotier network
###########################################################
chmod +x zerotier_connect.sh
./zerotier_connect.sh $input_network_id

#########################################################
# Confirm that everything is OK
#########################################################
echo "[ZEROTIER-DEPLOY: SUCCESS]"
