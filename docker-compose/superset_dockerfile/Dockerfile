FROM apache/superset:latest
 
USER root
 
# Обновление pip
RUN pip install --upgrade pip 
 
# Установка библиотеки psycopg2-binary, необходимой для подключения к PostgreSQL
RUN pip install psycopg2-binary
 
COPY ./superset-init.sh /superset-init.sh
COPY superset_config.py /app/
ENV SUPERSET_LOAD_EXAMPLES=no
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py
 
# Выдача прав на запуск
RUN chmod +x /superset-init.sh
 
USER superset
