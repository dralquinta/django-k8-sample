#!/bin/sh

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"dralquinta@gmail.com"}
cd /app/

/opt/venv/bin/python3 manage.py migrate --noinput 
/opt/venv/bin/python3 manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true 


