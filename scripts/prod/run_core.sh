#!/bin/bash
source setenv

WORKERS=2

echo "starting charles"
cd \/home\/onsa\/onsa\/core\/
gunicorn -b unix:/home/onsa/onsa/core/myproject.sock -w $WORKERS settings.wsgi