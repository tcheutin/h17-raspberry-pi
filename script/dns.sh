#!/bin/bash

###############################################################################
#
# Name        : dns.sh
# Author      : Nicolas De Oliveira Nadeau
# Usage       : ./dns.sh [-i Ip]
# Description : Base installation of bind9, DNS servicing
#

DIGIT=$(ifconfig eth0  | grep 'inet addr:'| \
      egrep '[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}' | \
      cut -d. -f4 | awk '{ print $1}')

IP="172.16.$DIGIT.1"

while getopts i: option
do
        if [ "${option}" == "i" ]; then
          IP=${OPTARG}
        fi
done

# Upgrade
apt-get update
apt-get upgrade -y

# We install dependancy
apt-get install -y bind9 bind9utils dnsutils

# we enable log
logging="
logging {
    channel bind.query.log {
        file \"/var/log/dns.query.log\";
        print-time yes;
        severity debug 3;
    };
    category queries { bind.query.log; };
};
"
echo $logging >> /etc/bind/named.conf.options
touch /var/log/dns.query.log
chown bind:bind /var/log/dns.query.log

# We create our own zones
namedConfLocal="
zone \"gti525.org\" {
    type master;
    file \"/etc/bind/zones/db.gti525.org\";
};
"
echo $namedConfLocal >> /etc/bind/named.conf.local

# We specifie our zone
mkdir /etc/bind/zones
sed -e "s/\${IP}/$IP/" config/db.gti525.org > /etc/bind/zones/db.gti525.org

# Restart service
/etc/init.d/bind9 restart
