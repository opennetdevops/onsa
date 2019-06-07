#!/bin/bash
source setenv

rootlevel=`eval "cd $PWD;cd ../..;pwd"`

cd \/home\/onsa\/onsa\/worker\/
celery -A worker worker --loglevel=info