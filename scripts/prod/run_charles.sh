#!/bin/bash
source setenv

WORKERS=2

echo "starting charles"
cd \/home\/onsa\/onsa\/charles\/
gunicorn -b 0.0.0.0:$CHARLES_PORT -w $WORKERS settings.wsgi
