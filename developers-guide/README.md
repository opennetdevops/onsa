# Guía para developers (running on local env)

## Requerimientos

Para desarrollar se necesitan ciertas librerías que deben estar instaladas.

* Python3 &gt;= 3.5.2
* PostgreSQL &gt;= 10.4
* pip3 &gt;= 19.0.3
* Ruby &gt;= 2.5.0
* Django &gt;= 2.1.8
* pyMongo &gt;= 3.7.2
* NodeJS &gt;= 10.10 
* npm &gt;= 6.4.1

Se recomienda un entorno con al menos:
* 4 vCPU
* 16 GB RAM


## Instalación BDs 

* PostgreSQL

```bash
$ sudo apt-get install postgresql postgresql-contrib
```
Source and detailed explanation:https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

* MongoDB
```bash
sudo apt install -y mongodb
sudo systemctl status mongodb
mongo --eval 'db.runCommand({ connectionStatus: 1 })'
```
Source and detailed explanation: https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-18-04

## Inicialización de Ruby (con rbenv)
```bash
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
type rbenv
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
rbenv install -l
rbenv install 2.5.1
ruby -v
echo "gem: --no-document" > ~/.gemrc
gem update --system
gem install bundler
rbenv global 2.5.1
ruby -v
echo "gem: --no-document" > ~/.gemrc
gem env home
gem install rails
rbenv rehash
rails -v
```
Source and detailed explanation: https://www.digitalocean.com/community/tutorials/how-to-install-ruby-on-rails-with-rbenv-on-ubuntu-18-04

## Instalación Django
Refresh the local package index.
```bash
sudo apt update
```
Check the version of Python you have installed (should be 3.5.2 or above):
```bash
python3 -V
```
Install PIP from Ubuntu repositories:
```bash
sudo apt install python3-pip
```
Install Django using PIP to get a scpecific version:
```bash
pip install Django==2.1.8
```
Source and detailed explanation: https://www.digitalocean.com/community/tutorials/how-to-install-the-django-web-framework-on-ubuntu-18-04


## Instalación NodeJS / NPM
```bash
sudo apt install nodejs
sudo apt install npm
```
Source and detailed explanation: https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-18-04



## Inicialización de la base de datos

#### Ingresar a la consola de postgres

```bash
$ sudo su
$ psql postgres
```
o bien 

```bash
sudo -u postgres psql
```

#### Crear DB

El core ONSA (EzWAN) emplea PostgreSQL, crear las siguientes DB:
```sql
CREATE ROLE automation with login password 'F1b3rc0rp';
CREATE database onsa;
ALTER role automation SET client_encoding TO 'utf8';
ALTER role automation SET default_transaction_isolation TO 'read committed';
ALTER role automation SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE onsa to automation;
ALTER USER automation WITH SUPERUSER;
\q
```
El modulo r-inventory si bien usa PostgreSQL se conecta desde ruby con lo cual la creacion se debe ejecutar desde rails:

```bash
rootlevel=`eval "cd $PWD;cd ../..;pwd"`
cd $rootlevel\/r-inventory\/
rails db:create
```
Nota: Si se desea desacoplar la base de r-inventory se debe modificar el archivo database.yaml

For a simplified install process you can just use create_db.sh script located at onsa/scripts/local


## Instalar dependencias

```bash
sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
cd onsa
sudo pip3 install -r requirements.txt
cd r-inventory
bundle install
cd onsa-dashboard
npm ci

```

## Inicialización de Django

```bash
cd onsa/scripts/local
. setenv
./run.sh
```

# 2-Day Operations

## Run services
```bash
cd onsa/scripts/local
./run.sh
```

## Stop services
```bash
cd onsa/scripts/local
./stop.sh
```

## Restart services
```bash
cd onsa/scripts/local
./restart.sh
```

