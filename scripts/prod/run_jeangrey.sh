#!/bin/bash
source setenv

WORKERS=2

echo "starting jeangrey"
cd \/home\/onsa\/onsa\/jeangrey\/
gunicorn -D -b 0.0.0.0:$JEANGREY_PORT -w $WORKERS settings.wsgi
