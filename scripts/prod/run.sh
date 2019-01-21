#!/bin/bash
WORKERS=3
BIND="0.0.0.0:8000"

python3 manage.py migrate
gunicorn -b $BIND settings.wsgi --workers $WORKERS