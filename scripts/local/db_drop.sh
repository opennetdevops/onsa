#!/bin/bash
set -e
set -u
RUN_PSQL="psql -X --set AUTOCOMMIT=off --set ON_ERROR_STOP=on postgres"
${RUN_PSQL} <<SQL
drop database onsa;
CREATE database onsa;
ALTER role automation SET client_encoding TO 'utf8';
ALTER role automation SET default_transaction_isolation TO 'read committed';
ALTER role automation SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE onsa to automation;
ALTER USER automation WITH SUPERUSER;
\q
SQL

rootlevel=`eval "cd $PWD;cd ../..;pwd"`
cd $rootlevel\/r-inventory\/
rails db:drop
rails db:create
