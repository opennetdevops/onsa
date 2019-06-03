#!/bin/bash
set -e
set -u
RUN_PSQL="sudo -u postgres -i psql -X --set AUTOCOMMIT=off --set ON_ERROR_STOP=on postgres"
${RUN_PSQL} <<SQL
drop database onsa;
\q
SQL
exit
