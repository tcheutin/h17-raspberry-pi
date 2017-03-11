#!/bin/bash

###############################################################################
#
# Name        : base.sh
# Author      : Nicolas De Oliveira Nadeau
# Usage       : ./base.sh
# Description :
#

# Update/upgrade
apt-get update
apt-get upgrade -y

# Install dependancy
apt-get install -y git python3 python3-pip

# We make sure we have the latest pip version
pip3 install --upgrade pip

# Make sure we use the right python version
echo "alias python='python3.4'" >> ~/.bashrc
source ~/.bashrc

# We clone the project
mkdir ~/src
git clone https://github.com/gti525/h17-raspberry-pi.git ~/src/

# Install project requirement
cd ~/src/h17-raspberry-pi
pip install -r requirement.txt

# We start the project
cd gti525
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
