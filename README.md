# vCPE


## Initialize PSQL Database settings

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
