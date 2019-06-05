#!/bin/bash
source setenv

rootlevel=`eval "cd $PWD;cd ../..;pwd"`
declare -a projects=("charles" "core" "jeangrey" "worker")

for project in "${projects[@]}"
do
    python3.6 $rootlevel\/$project\/manage.py migrate
done

# cd $rootlevel\/r-inventory\/
# rails db:migrate

cd ../scripts/local/



