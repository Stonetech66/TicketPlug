#!/bin/sh

set -e
cd /app/

echo " starting celery worker"
celery -A Event_Project worker -l info -c 1
