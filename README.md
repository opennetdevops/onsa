# vCPE

## Install PSQL Database
### Ubuntu

`sudo apt-get install postgresql postgresql-contrib`

### macOS

brew install postgresql

## Initialize PSQL Database settings

`sudo su postgres`

`psql postgres`
 
 ### Create user nsx
`CREATE ROLE nsx with login password 'F1b3rc0rp';`

### Create vcpe database
`CREATE database vcpe;`

### User config
`ALTER role nsx SET client_encoding TO 'utf8';`

`ALTER role nsx SET default_transaction_isolation TO 'read committed';`

`ALTER role nsx SET timezone TO 'UTC';`

### Grant privileges

`GRANT ALL PRIVILEGES ON DATABASE vcpe to nsx;`

## Django initialization

`sudo pip3 install -r requirements.txt`

### Create Django user

`python3 manage.py createsuperuser`

### Django create migrations

`python3 manage.py makemigration`

### Django apply migrations

`python3 manage.py migrate`

### Django run server

`python3 manage.py runserver`

### Comments

Modify in `settings.py`: `TEMPLATES = [{'DIRS': '/<insert-path>/vCPE/vCPE/nsx/templates'}]`
