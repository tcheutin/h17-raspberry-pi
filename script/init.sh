#!/bin/bash

###############################################################################
#
# Name        : init.sh
# Author      : Nicolas De Oliveira Nadeau
# Usage       : ./init.sh
# Description : Default script that launch all setup scripts
#

# We update our system
apt-get update
apt-get upgrade -y


# We launch all setup scripts
./dhcp.sh
./wifi.sh
./nginx.sh
./dns.sh
./base.sh
