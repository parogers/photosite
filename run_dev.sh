#!/bin/bash

IP=`hostname -I|tr -d ' '|head -1`

if [ "$IP" = "" ]; then
    echo "can't figure out IP address"
    exit
fi

export PHOTOSITE_ALLOWED_HOSTS="$IP"
export PHOTOSITE_CONTENT_SERVER="$IP"

echo ""
echo "###BINDING TO IP $IP"
echo ""
./manage.py runserver "${IP}:8000"
