#!/bin/bash
 
# Инициализация базы данных Superset
superset db upgrade
 
# Создание учетной записи администратора
superset fab create-admin \
    --username "${ADMIN_USERNAME}" \
    --firstname Superset \
    --lastname Admin \
    --email "${ADMIN_EMAIL}" \
    --password "${ADMIN_PASSWORD}"
 
superset init
 
# Ожидание пока Superset поднимется
sleep 90
 
# Загрузка примерных данных (если необходимо)
# superset load_examples
 
# Добавление подключения к внешней базе данных PostgreSQL
superset dbs add \
  --database-name hh_data_engineer \
  --sqlalchemy-uri postgresql+psycopg2://airflow:airflow@postgres:5432/hh_data_engineer \
  --configuration-method sql \
