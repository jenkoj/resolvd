#!/bin/bash

while true
do
        (! ping -c1 google.com >/dev/null 2>&1 ) && (systemctl restart lte-modem.service)
        sleep 60
done
