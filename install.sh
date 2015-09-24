#!/usr/bin/bash

command -v pip > /dev/null
if [ $? -eq 0 ]
then
    pip2 install -r requirements.txt
    echo "You should see the settings file before running the servers."
else
    echo "You need to install pip2 first."
fi
