#!/bin/bash
source setenv

rootlevel=`eval "cd $PWD;cd ../..;pwd"`

declare -a projects=("charles" "core" "inventory" "jeangrey" "worker")

for project in "${projects[@]}"
do
    echo "starting $project"
    python3 $rootlevel\/$project\/manage.py migrate
    python3 $rootlevel\/$project\/manage.py loaddata $rootlevel\/$project\/$project\/fixtures\/local\/*
    port=$(echo "$project" | tr '[:lower:]' '[:upper:]')_PORT
    python3 $rootlevel\/$project\/manage.py runserver 127.0.0.1:${!port} &

done

#python3 $rootlevel\/$projects\/manage.py createsuperuser


