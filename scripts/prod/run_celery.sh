#!/bin/bash
source setenv

rootlevel=`eval "cd $PWD;cd ../..;pwd"`

cd \/home\/onsa\/onsa\/worker\/
echo "starting celery"

celery -A worker worker --loglevel=info