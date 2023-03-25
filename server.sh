#!/usr/bin/env bash
set -e
cd /app
echo "starting migrations"
python manage.py makemigrations
python manage.py migrate --noinput

echo "collecting staticfiles"

python manage.py collectstatic --noinput

echo "starting server 🚀"
gunicorn Event_Project.wsgi:application --bind 0.0.0.0:8000
