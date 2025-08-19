# HH_ETL_Pipeline

![ETL_schema](https://github.com/Alya-DE/HH_ETL_Pipeline/blob/main/png/ETL_schema.png)

---
### Цель
Разработать ETL-процесс, который ежедневно забирает данные по ключевым словам из публичного API hh.ru, загружает их в хранилище данных PostgreSQL и ежедневно обновляет дашборд в Apache Superset.

---
### Структура проекта
```
.
├── docker-compose.yml
├── airflow_dockerfile
│   └── Dockerfile
│   └── requirements.txt
├── dags
├── superset_dockerfile
├── src
│   └── init_db
│          └── init.sql
└── .env
```

---
### Стек и версии:

|    Компонент    |               Версия              |     Порт(ы)     |
| --------------- | :-------------------------------: | :-------------: |
| Ubuntu          |               24.04               |        -        |
| Docker          |               28.2.2              |        -        |
| Docker Compose  |               2.36.2              |        -        |
| Apache Airflow  |               2.10.2              |       8080      |
| PostgreSQL      |            postgres:15            |       5432      |
| Apache Superset |               4.1.3               |       8088      |

---
### Сети - настройка портов на удаленной виртуальной машине
В проекте инфраструктура была развернута на удаленной виртуальной машине [cloud.ru](https://cloud.ru/), поэтому дополнительно потребовалось настроить правила входящего трафика для Airflow и Superset для соответствующей группы безопасности:

![VM_rules.png](https://github.com/Alya-DE/HH_ETL_Pipeline/blob/main/png/VM_rules.png)

После успешного развертывания доступно подключение:
```
http://<public-ip>:8080   # Airflow
http://<public-ip>:8088   # Superset
```

---
### Установка и запуск
1. Клонирование репозитория
```bash
git clone https://github.com/Alya-DE/HH_ETL_Pipeline.git
cd HH_ETL_Pipeline
```

2. Создание файла `.env` с параметрами:
```env
POSTGRES_USER=airflow 
POSTGRES_PASSWORD=airflow
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=password
AIRFLOW_UID=501
AIRFLOW_GID=0 
SUPERSET_ADMIN_USERNAME=admin 
SUPERSET_ADMIN_EMAIL=admin@superset.com 
SUPERSET_ADMIN_PASSWORD=supersecret123 
SUPERSET_SECRET_KEY=<результат_функции_secrets.token_urlsafe(32)> # потребуется сгенерировать уникальный 32-байтный секретный ключ
```

3. Запуск проекта из корневой директории с помощью docker compose:
```bash
sudo docker compose build
sudo docker compose up -d
```

Проверка успешной установки через статусы контейнеров:
```bash
sudo docker compose ps -a
```

---
### Возможные проблемы при развертывании и решения:
#### *1) Airflow не стартует, ругается на logs/права*

В процессе установки создается директория `./logs` для airflow. Может потребоваться выдача прав доступа для этой папки:
```bash
sudo mkdir -p ./logs
sudo chown -R 501:0 ./logs
```

После необходимо перезапустить docker compose:
```bash
sudo docker compose down
sudo docker compose up -d
```

#### *2) База метаданных Superset не создалась автоматически*
В случае возникновения ошибки с автоматическим созданием базы данных для метаданных Apache Superset, может потребоваться ручная установка необходимой БД. Для этого:
```
# заходим в работающий контейнер Postgres под root-пользователем БД
docker exec -it hh_data_engineer-postgres-1 psql -U ${POSTGRES_USER}

# Внутри psql создаем необходимую базу данных:
CREATE DATABASE superset_meta OWNER airflow;
\q

# После осуществляем локальный перезапуск контейнеров superset-init и superset:
docker compose up -d superset-init
docker compose up -d superset
```

---
### Настройка дашборда.
Apache Superset предлагает широкий спектр настройки для динамических дашбордов. В дашборде проекта я хотела отразить актуальные данные по вакансиям "Data Engineer" с локализацией в городе Москва и с опытом работы от 0 до 3 лет ровно за последние 30 дней публикации. Для этого в SQL Lab была настроена схема, из которой в последующем были взяты данные для построения дашборда:

```sql
SELECT *
FROM vacancies 
WHERE published_at >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY published_at DESC;
```

### Пример дашборда:
![dashboard.png](https://github.com/Alya-DE/HH_ETL_Pipeline/blob/main/png/dashboard.png) 
