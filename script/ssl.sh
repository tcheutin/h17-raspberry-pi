#!/bin/bash

###############################################################################
#
# Name        : ssl.sh
# Author      : Nicolas De Oliveira Nadeau
# Usage       : ./ssl.sh
# Description : Allow HTTPS with NGINX
# REFERENCE   : https://gist.github.com/jessedearing/2351836
#

# Update/upgrade
apt-get update
apt-get upgrade -y

# Install dependancy
apt-get install -y openssl

# Generate a passphrase
PASSPHRASE=$(head -c 500 /dev/urandom | tr -dc a-z0-9A-Z | head -c 128; echo)

# Certificate details
subj="
C=CA
ST=QC
L=Montreal
O=ehall.gti525.org
CN=ehall
OU=RaspberryPi
"
# Generating an SSL private key to sign your certificate
openssl genrsa -des3 -out ehall.key -passout pass:$PASSPHRASE 2048

# Generating a Certificate Signing Request
openssl req -new -batch \
            -key ehall.key \
            -out ehall.csr \
            -passin pass:$PASSPHRASE \
            -subj $(echo -n "$subj" | tr "\n" "/")

# Removing passphrase from key (for nginx)
openssl rsa -in ehall.key \
            -out ehall.key \
            -passin pass:$PASSPHRASE

# Generating certificate
openssl x509 -req -days 3650 \
                  -in ehall.csr \
                  -signkey ehall.key \
                  -out ehall.crt

# Generating strong Diffie-Hellman. Very Slow on Pi ...
# For now, we will use a pre-made file [DEV]
# openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
cp config/dhparam.pem /etc/ssl/certs/

# Copying certificate (ehall.crt) to /etc/ssl/certs/
mkdir -p  /etc/ssl/certs
cp ehall.crt /etc/ssl/certs/

# Copying key (ehall.key) to /etc/ssl/private/
mkdir -p  /etc/ssl/private
cp ehall.key /etc/ssl/private/
