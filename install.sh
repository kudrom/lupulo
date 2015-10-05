#!/usr/bin/bash

echo "THIS SCRIPT IS GUARANTED TO WORK ONLY ON ARCH DISTRIBUTIONS"
command -v pip2 > /dev/null
if [ $? -eq 0 ]
then
    pip2 install -r requirements.txt
    echo "You should see the settings file before running the servers."
else
    echo "You need to install pip2 first."
fi
