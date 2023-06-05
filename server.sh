#!/bin/sh

set -e
cd /app


echo "starting migrations"
python manage.py makemigrations

echo "creating superuser"

python manage.py createsuperuser --noinput | | true

echo "collecting server"

python manage.py collectstatic --noinput

echo "starting server 🚀"
gunicorn Event_Project.wsgi:application --bind 0.0.0.0:8000
