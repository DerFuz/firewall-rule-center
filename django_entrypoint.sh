#!/bin/sh

echo 'Waiting for DB...'

DB_HOSTNAME=$(echo $DJANGO_DATABASE_URL | awk -F '[@/:]' '{print $6}')
DB_PORT=$(echo $DJANGO_DATABASE_URL | awk -F '[@/:]' '{print $7}')

echo $DB_HOSTNAME $DB_PORT

while ! nc -z $DB_HOSTNAME $DB_PORT; do
    sleep 0.1
done

echo 'DB started'

echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

exec "$@"