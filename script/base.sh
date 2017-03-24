#!/bin/bash

###############################################################################
#
# Name        : base.sh
# Author      : Nicolas De Oliveira Nadeau
# Usage       : ./base.sh
# Description : Default project setup, by now, everything should work!
#

# Update/upgrade
apt-get update
apt-get upgrade -y

# Install dependancy
apt-get install -y git python3 python3-pip sqlite3

# Git config
git config --global user.name "Pi Raspberry"
git config --global user.email pi@gti525.org

# We make sure we have the latest pip version
pip3 install --upgrade pip

# Make sure we use the right python version
echo "alias python='python3.4'" >> ~/.bashrc
source ~/.bashrc

# We save the current folder to store it in the service folder
cd ..
FOLDER=$(pwd)

# Install project requirement
pip install -r requirement.txt

# We start the project
cd gti525
sed -e "s/\${FOLDER}/'$FOLDER'/" config/ehall.init > /etc/init.d/ehall.init
chmod +x /etc/init.d/ehall.init

######### REMOVE - FOR DEV ONLY #########
# Insert API_KEY into BD
sqlite3 db.sqlite3 "INSERT INTO rest_framework_api_key_apikey \
        VALUES (\"\", \"\", \"\", \"\", \"a677abfcc88c8126deedd719202e50922\");"
