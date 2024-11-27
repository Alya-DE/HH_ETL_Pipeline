import os    
from datetime import timedelta
from superset.config import *

# Основные настройки
SECRET_KEY = 'YOUR_SECRET_KEY' # YOUR_SECRET_KEY сгенерируем заранее с помощью команды openssl rand -base64 42

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://airflow:airflow@postgres:5432/hh_data_engineer' 

# Настройки безопасности
CSRF_ENABLED = True  # Включим защиту CSRF
WTF_CSRF_ENABLED = True  # Включим CSRFзащиту для форм, реализованных с использованием Flask-WTF
WTF_CSRF_TIME_LIMIT = None  # Установим лимит времени для токена CSRF 