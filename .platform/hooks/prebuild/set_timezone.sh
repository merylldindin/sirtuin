#!/bin/bash

NEWTIMEZONE="$(/opt/elasticbeanstalk/bin/get-config environment -k TZ)"

if [ -z $NEWTIMEZONE ] ; then
    echo "TZ" environment property not set
    exit 1
fi

if [ ! -f /usr/share/zoneinfo/$NEWTIMEZONE ] ; then
    echo /usr/share/zoneinfo/$NEWTIMEZONE does not exist
    exit 1
fi

timedatectl set-timezone $NEWTIMEZONE
