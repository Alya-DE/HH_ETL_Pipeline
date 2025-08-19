CREATE DATABASE hh_data_engineer OWNER airflow;

CREATE DATABASE airflow OWNER airflow;

CREATE DATABASE superset_meta
  WITH OWNER = airflow
  ENCODING = 'UTF8'
  CONNECTION LIMIT = -1;
