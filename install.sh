#!/usr/bin/bash

ID=`id -u`
if [ $ID -ne 0 ]
then
    echo "You must be root in order to run this script."
    exit -1
fi

command -v pacman > /dev/null
if [ $? -eq 0 ]
then
    mkdir log 2> /dev/null
    chmod 777 log

    pacman --noconfirm -S base-devel

    pacman --noconfirm -S mongodb
    systemctl enable mongodb
    systemctl start mongodb

    pacman --noconfirm -S python2 python2-pip
    pip2 install -r requirements.txt

    echo "INSTALLATION COMPLETE"
    echo "You should see the settings file before running the servers."
else
    echo "This script only works on arch distributions."
fi
