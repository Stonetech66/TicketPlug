#!/usr/bin/env bash
set -e

cd /app

echo " starting celery worker"
celery - A Event_Project worker -l info -c $NO_WORKER
