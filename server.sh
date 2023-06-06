#!/usr/bin/env bash
cd /app/

echo "starting migrations"
python manage.py makemigrations
python manage.py migrate

echo 'creating superuser'
python manage.py createsuperuser --email ${DJANGO_SUPERUSER_EMAIL} --noinput

echo 'collecting staticfiles'
python manage.py collectstatic --noinput

echo "starting server 🚀"

gunicorn Event_Project.wsgi:application --bind 0.0.0.0:8000
