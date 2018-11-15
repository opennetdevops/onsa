# Guía para developers

## Requerimientos

Para desarrollar se necesitan ciertas librerías que deben estar instaladas.

* Python3
* PostgreSQL
* pip3

## Instalación

Primero se debe verificar que la versión de python3 sea &gt;= 3.5.2.

```bash
$ python3 --version
Python 3.5.2
```

Lo siguiente es instalar pip3 en el OS y PostgreSQL.

* Ubuntu

```bash
$ sudo apt-get install postgresql postgresql-contrib
```

* macOS

```bash
$ brew install postgresql
```

## Inicialización de la base de datos

#### Ingresar a la consola de postgres

```bash
$ sudo su
$ psql postgres
```

#### Crear DB

```sql
CREATE ROLE automation with login password 'F1b3rc0rp';
CREATE database onsa;
ALTER role automation SET client_encoding TO 'utf8';
ALTER role automation SET default_transaction_isolation TO 'read committed';
ALTER role automation SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE onsa to automation;
```

## Instalar dependencias

```bash
$ cd ONSA
sudo pip3 install -r requirements.txt
```

## Inicialización de Django

```bash
$ cd ONSA/ONSA
$ python3 manage.py createsuperuser # Creates admin user
Username:
$ python3 manage.py makemmigrations # Makes migrations
$ python3 manage.py migrate # Runs migrations
$ python3 manage.py runserver # Start server
```



