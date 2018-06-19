---
description: Guía para el desarrollo de la aplicación.
---

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

{% hint style="info" %}
Ubuntu
{% endhint %}

```bash
$ sudo apt-get install postgresql postgresql-contrib
```

{% hint style="info" %}
macOS
{% endhint %}

```bash
$ brew install postgresql
```

## Inicialización de la base de datos

#### Ingresar a la consola de postgres

```bash
$ sudo su
$ psql postgres
```

#### Crear usuario nsx

```sql
$ CREATE ROLE nsx with login password 'F1b3rc0rp';
```

#### Crear base de datos

```sql
$ CREATE database vcpe;
```

#### Configuración de usuario

```sql
$ ALTER role nsx SET client_encoding TO 'utf8';
$ ALTER role nsx SET default_transaction_isolation TO 'read committed';
$ ALTER role nsx SET timezone TO 'UTC';
```

#### Dar privilegios al usuario

```sql
$ GRANT ALL PRIVILEGES ON DATABASE vcpe to nsx;
```

## Instalar dependencias

```bash
$ cd vCPE
sudo pip3 install -r requirements.txt
```

## Inicialización de Django

```bash
$ cd vCPE/vCPE
$ python3 manage.py createsuperuser # Creates admin user
Username:
$ python3 manage.py makemmigrations # Makes migrations
$ python3 manage.py migrate # Runs migrations
$ python3 manage.py runserver # Start server
```



