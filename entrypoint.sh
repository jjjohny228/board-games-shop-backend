#!/usr/bin/env bash
# exit on error
set -o errexit

python manage.py migrate

# run web server
gunicorn config.wsgi --bind 0.0.0.0:8000 --access-logfile -
