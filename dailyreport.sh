#!/bin/sh

touch /tmp/dailyreport.log
echo "0 10 * * * python /home/app/manage.py dailyreport >> /tmp/dailyreport.log 2>&1" > /etc/crontabs/root
crond start
tail -f /tmp/dailyreport.log