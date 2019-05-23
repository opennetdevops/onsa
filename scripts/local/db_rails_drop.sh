rootlevel=`eval "cd $PWD;cd ../..;pwd"`
cd $rootlevel\/r-inventory\/
echo "dropping rails db"
rails db:drop