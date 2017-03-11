#!/bin/bash

###############################################################################
#
# Name        : nginx.sh
# Author      : Nicolas De Oliveira Nadeau
# Usage       : ./nginx.sh [-p PASSWORD]
# Description : Basic installation of Nginx with our own config
#

# SSL script MUST be run BEFORE this script

# Update/upgrade
apt-get update
apt-get upgrade -y

# Install dependancy
apt-get install -y nginx

# We remove default Site config
rm /etc/nginx/sites-enabled/default

# We add our custom config
cp config/ehallReverse.conf /etc/nginx/sites-enabled/

# We restart the Nginx service
service nginx restart
