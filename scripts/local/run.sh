#!/bin/bash
source setenv

rootlevel=`eval "cd $PWD;cd ../..;pwd"`

declare -a projects=("charles" "core" "inventory" "jeangrey" "worker")
starting_port=8000


for project in "${projects[@]}"
do
    echo "starting $project"
    python3 $rootlevel\/$project\/manage.py migrate
    python3 $rootlevel\/$project\/manage.py loaddata $rootlevel\/$project\/$project\/fixtures\/local\/*
    python3 $rootlevel\/$project\/manage.py runserver 127.0.0.1:$starting_port &
    let "starting_port++"
done

python3 $rootlevel\/$projects\/manage.py createsuperuser


