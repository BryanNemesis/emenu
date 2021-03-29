#!/bin/sh

touch /home/dailyreport.log
echo "0 10 * * * python /home/app/manage.py dailyreport >> /home/dailyreport.log 2>&1" > /etc/crontabs/root
crond start
tail -f /home/dailyreport.log