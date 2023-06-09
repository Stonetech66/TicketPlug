#!/usr/bin/env bash 
cd /app/



echo "starting celery >>>"

celery -A Event_Project worker -l info -c 2
