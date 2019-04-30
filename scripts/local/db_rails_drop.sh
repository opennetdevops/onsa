rootlevel=`eval "cd $PWD;cd ../..;pwd"`
cd $rootlevel\/r-inventory\/
rails db:drop
rails db:create