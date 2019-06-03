#!/bin/bash
source setenv
rootlevel=`eval "cd $PWD;cd ../..;pwd"`

cd $rootlevel\/worker\/
celery -A worker worker --loglevel=info &

cd ../scripts/local/



