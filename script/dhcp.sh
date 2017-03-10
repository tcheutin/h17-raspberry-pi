#!/bin/bash

###############################################################################
#
# Name        : dhcp.sh
# Author      : Nicolas De Oliveira Nadeau
# Usage       : ./dhcp.sh [-i SpecificIpRange]
# Description :
#

DEFAULT_INTERFACE_CONFIG="/etc/network/interfaces"
DEFAULT_DHCPD_CONFIG="/etc/dnsmasq.conf"

IP="1"
NETMASK="255.255.255.0"

while getopts i: option
do
        if [ "${option}" == "i" ]; then
          IP=${OPTARG}
        fi
done


################################# INTERFACE ################################
IP="172.16.$IP"
echo $IP

# We make a backup of the file.
yes | cp -rf $DEFAULT_INTERFACE_CONFIG config/interfaces.ORIGINAL

# We fill our template with our IP range
sed -e "s/\${IP}/'$IP.1'/" -e "s/\${NETMASK}/$NETMASK/" config/interfaces > $DEFAULT_INTERFACE_CONFIG

# Down/Up interfaces
ifdown wlan0
ifup wlan0


################################# DHCPD ################################
# Update/Upgrade
apt-get update
apt-get -y upgrade

# Install isc-dhcp-server
apt-get install -y dnsmasq

# We make a backup of the file.
yes | cp -rf $DEFAULT_DHCPD_CONFIG config/dnsmasq.conf.ORIGINAL

# We fill our template with our IP range
sed -e "s/\${IP}/'$IP'/" config/dnsmasq.conf > $DEFAULT_DHCPD_CONFIG

# Start service
service dnsmasq start
