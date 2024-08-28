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
echo "Connecting to network id: $input_network_id"

sudo zerotier-cli join "$input_network_id"

echo "zerotier-connect completed. Connected zerotier networks:" && sudo zerotier-cli listnetworks
