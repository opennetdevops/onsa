./stop.sh
sleep 2
./db_django_drop.sh
sleep 2
./db_rails_drop.sh
sleep 2
./create_db.sh
sleep 2
./migrate.sh
sleep 2
./run.sh
