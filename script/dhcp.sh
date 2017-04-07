#!/bin/bash

###############################################################################
#
# Name        : dhcp.sh
# Author      : Nicolas De Oliveira Nadeau
# Usage       : ./dhcp.sh [-i SpecificIpRange]
# Description : Setup the DHCP service for the wifi access
#

DEFAULT_INTERFACE_CONFIG="/etc/network/interfaces"
DEFAULT_DHCPD_CONFIG="/etc/dnsmasq.conf"

DIGIT=$(ifconfig eth0  | grep 'inet addr:'| \
      egrep '[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}' | \
      cut -d. -f4 | awk '{ print $1}')

IP="172.16.$DIGIT.1"
NETMASK="255.255.255.0"

while getopts i: option
do
        if [ "${option}" == "i" ]; then
          IP=${OPTARG}
        fi
done


################################# INTERFACE ################################
# We make a backup of the file.
yes | cp -rf $DEFAULT_INTERFACE_CONFIG config/interfaces.ORIGINAL

# We fill our template with our IP range
sed -e "s/\${IP}/$IP/" -e "s/\${NETMASK}/$NETMASK/" \
        config/interfaces > $DEFAULT_INTERFACE_CONFIG

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

IP=$(echo $IP| cut -d. -f1-3 | awk '{ print $1 }')
# We fill our template with our IP range
sed -e "s/\${IP}/$IP/" config/dnsmasq.conf > $DEFAULT_DHCPD_CONFIG

# Start service
service dnsmasq start
