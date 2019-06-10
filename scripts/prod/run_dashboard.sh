#!/bin/bash
source setenv

rootlevel=`eval "cd $PWD;cd ../..;pwd"`
echo "starting dashboard"

cd \/home\/onsa\/onsa\/onsa-dashboard\/
serve -s build