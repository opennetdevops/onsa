#!/bin/bash
source setenv
rootlevel=`eval "cd $PWD;cd ../..;pwd"`

cd $rootlevel\/onsa-dashboard\/
npm start &

cd ..
cd scripts/local/

