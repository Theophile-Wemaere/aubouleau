#!/bin/sh

# Seems to be the only way to change the timezone used by cron
unlink /etc/localtime
ln -s /usr/share/zoneinfo/Europe/Paris /etc/localtime
# Copy root environment variables to root's crontab
printenv > /var/spool/cron/crontabs/root
service cron start

python manage.py flush --no-input
python manage.py makemigrations aubouleau_web
python manage.py migrate
python manage.py loaddata initial
python manage.py crontab add
# TODO: Find a way to force the cronjob to run on first launch

exec "$@"
