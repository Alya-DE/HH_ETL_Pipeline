import os    
from datetime import timedelta
 
# Основные настройки
SECRET_KEY = os.getenv('SUPERSET_SECRET_KEY', 'mYSECRETkey_123')
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://airflow:airflow@postgres:5432/superset_meta' 
THUMBNAILS_ENABLED = True
THUMBNAILS_SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI

# Настройки безопасности
CSRF_ENABLED = True  # Включим защиту CSRF
WTF_CSRF_ENABLED = True  # Включим CSRF защиту для форм, реализованных с использованием Flask-WTF
WTF_CSRF_TIME_LIMIT = None  # Установим лимит времени для токена CSRF 
