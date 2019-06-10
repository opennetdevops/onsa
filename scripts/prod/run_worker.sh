#!/bin/bash
source setenv

WORKERS=2

echo "starting worker"
cd \/home\/onsa\/onsa\/worker\/
gunicorn -b 0.0.0.0:$WORKER_PORT -w $WORKERS settings.wsgi