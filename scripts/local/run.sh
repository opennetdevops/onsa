#!/bin/bash
source setenv

rootlevel=`eval "cd $PWD;cd ../..;pwd"`

#declare -a projects=("charles" "core" "inventory" "jeangrey" "worker")
declare -a projects=("charles" "core" "jeangrey" "worker")

for project in "${projects[@]}"
do
    echo "starting $project"
    python3 $rootlevel\/$project\/manage.py migrate
    python3 $rootlevel\/$project\/manage.py loaddata $rootlevel\/$project\/$project\/fixtures\/local\/*
    port=$(echo "$project" | tr '[:lower:]' '[:upper:]')_PORT
    python3 $rootlevel\/$project\/manage.py runserver 0.0.0.0:${!port} &

done

cd $rootlevel\/r-inventory\/
rails db:migrate
rails db:seed
rails s -b 0.0.0.0 -p $INVENTORY_PORT &

cd $rootlevel\/onsa-projects\/
./app.py &


#cd $rootlevel\/onsa-dashboard\/
#npm start &

cd ..
cd scripts/local/


#python3 $rootlevel\/$projects\/manage.py createsuperuser


