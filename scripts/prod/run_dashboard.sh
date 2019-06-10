#!/bin/bash
source setenv

rootlevel=`eval "cd $PWD;cd ../..;pwd"`

cd \/home\/onsa\/onsa\/onsa-dashboard\/
serve -s build