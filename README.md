# vCPE


#initialize PSQL Database settings

psql postgres
 
CREATE ROLE nsx with login password 'F1b3rc0rp';
CREATE database vcpe;
ALTER role nsx SET client_encoding TO 'utf8';
ALTER role nsx SET default_transaction_isolation TO 'read committed';
ALTER role nsx SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE vcpe to nsx;
