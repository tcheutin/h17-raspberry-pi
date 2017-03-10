#!/bin/bash

###############################################################################
#
# Name        : wifi.sh
# Author      : Nicolas De Oliveira Nadeau
# Usage       : ./wifi.sh [-p PASSWORD]
# Description : Deployement script to enable a basic Access Point for mobile
#               users. THIS DO NOT GIVE DHCP OR DNS OR INTERNET ACCESS
#

DEFAULT_FOLDER="/etc/hostapd/"
DEFAULT_CONFIG_FILE="hostapd.conf"

PASSWORD="passphrase"

while getopts p: option
do
        if [ "${option}" == "p" ]; then
          PASSWORD=${OPTARG}
        fi
done

# We do basic update
apt-get update
apt-get upgrade -y

# Installing the real thing
apt-get install - y hostapd

# We copy our default config file
cp config/$DEFAULT_CONFIG_FILE $DEFAULT_FOLDER$DEFAULT_CONFIG_FILE

# We add the passphrase for the wifi (it can be change)
echo 'wpa_passphrase='$PASSWORD >> $DEFAULT_FOLDER/$DEFAULT_CONFIG_FILE
