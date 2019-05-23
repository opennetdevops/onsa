#!/bin/bash
source setenv

rootlevel=`eval "cd $PWD;cd ../..;pwd"`
declare -a projects=("charles" "core" "jeangrey" "worker")

for project in "${projects[@]}"
do
    python3 $rootlevel\/$project\/manage.py migrate
    python3 $rootlevel\/$project\/manage.py loaddata $rootlevel\/$project\/$project\/fixtures\/local\/*
done

cd $rootlevel\/r-inventory\/
rails db:migrate
rails db:seed


cd ../scripts/local/




