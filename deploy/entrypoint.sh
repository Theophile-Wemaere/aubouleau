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
# Adds the cronjob to the crontab and stores the result in the variable below
crontab_add_output=$(python manage.py crontab add)
echo "$crontab_add_output"
# The crontab hash is extracted using this (not so great) hack
cronjob_hash=$(echo $crontab_add_output | cut -d '(' -f2 | cut -d ')' -f1)
# We then manually start the cronjob once
echo "Starting cronjob $cronjob_hash..."
python manage.py crontab run $cronjob_hash

exec "$@"
