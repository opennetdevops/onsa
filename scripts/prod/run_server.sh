#!/bin/bash
source setenv

WORKERS=2
rootlevel=`eval "cd $PWD;cd ../..;pwd"`

declare -a projects=("charles" "jeangrey" "worker")

for project in "${projects[@]}"
do
    echo "starting $project"
    port=$(echo "$project" | tr '[:lower:]' '[:upper:]')_PORT
    cd $rootlevel\/$project\/
    gunicorn -D -b 0.0.0.0:${!port} -w $WORKERS settings.wsgi
done

cd $rootlevel\/core\/
gunicorn -D -b unix:/home/onsa/onsa/core/myproject.sock -w $WORKERS settings.wsgi

cd $rootlevel\/onsa-dashboard\/
serve -s build &

cd ..
cd scripts/local/




