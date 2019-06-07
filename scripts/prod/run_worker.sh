#!/bin/bash
source setenv

WORKERS=2

echo "starting worker"
cd \/home\/onsA\/onsa\/worker\/
gunicorn -D -b 0.0.0.0:$WORKER_PORT -w $WORKERS settings.wsgi