from airflow import DAG  
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import requests  
import psycopg2  

# Определение DAG
dag = DAG(
    dag_id='hh_data_engineer_elt',
    start_date=datetime.now() - timedelta(days=1),  
    schedule_interval='@daily',  # DAG будет запускаться ежедневно и подгружать данные за предыдущий день
)

# Функция для создания таблицы для сохранения извлекаемых данных
def create_table_vacancies():  
    # Подключаемся к базе данных PostgreSQL - hh_data_engineer:
    connection = psycopg2.connect(          
        dbname='hh_data_engineer',
        user='worker',
        password='password',
        host='localhost',
        port='5432'
    )
    cursor = connection.cursor()    

    # Создадим таблицу vacancies, в которую будем вставлять данные, если она еще не существует:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY,
            title VARCHAR(50),
            salary_from INTEGER,
            salary_to INTEGER,
            experience VARCHAR(50),
            published_at DATE
        )
    """)
    connection.commit()  # Сохраняем изменения в базе данных
    cursor.close()  # Закрываем курсор
    connection.close()  # Закрываем соединение с базой данных

# Функция для извлечения данных из API
def extract_data_from_api(start_date, end_date):  
    api_url = f"https://api.hh.ru/vacancies?text=data%20engineer&area=1&per_page=100&date_from={start_date}&date_to={end_date}&experience=between1And3&experience=noExperience"  # Формируем URL для извлечения данных за определенный период
    response = requests.get(api_url) 
    
    if response.status_code == 200:  # Проверяем, успешен ли HTTP-запрос.
        vacancies_json = response.json()  # Преобразуем ответ в JSON
        return vacancies_json['items']  # Возвращаем список вакансий
    else:
        raise Exception("Ошибка при получении данных из API")  

# Функция для извлечения исторических данных
def load_historical_data_to_db():
    # Обозначим период, за который требуется извлечение исторических данных в формате YYYY-MM-DD:  
    start_date = '2025-03-01'
    end_date = '2025-03-27'

    # Извлекаем данные за указанный период
    vacancies = extract_data_from_api(start_date, end_date)

    # Подключаемся к базе данных PostgreSQL - hh_data_engineer
    connection = psycopg2.connect(
        dbname='hh_data_engineer',
        user='worker',
        password='password',
        host='localhost',
        port='5432'  
    )
    cursor = connection.cursor()

    for item in vacancies:  # Извлекаем список вакансий
        # Извлекаем необходимые данные о вакансии
        hh_vacancy_id = item.get("id")  # ID вакансии с сайта hh.ru
        vacancy_title = item.get("name")[:50] if item.get("name") else None  # Название вакансии
        salary = item.get("salary")
        salary_from = salary.get("from") if salary else None  # Минимальная зарплата
        salary_to = salary.get("to") if salary else None  # Максимальная зарплата
        experience = item.get("experience") 
        experience_requirements = experience.get("name") if experience else None  # Требования к опыту работы
        date_of_publish = item.get("published_at")  # Дата публикации вакансии
  
        # Выполним преобразование date_of_publish в формат DATE
        if date_of_publish:
            # Преобразуем строку к объекту типа date
            date_of_publish = datetime.strptime(date_of_publish, "%Y-%m-%dT%H:%M:%S%z").date()

        # Вставляем данные в таблицу vacancies в базе данных PostgreSQL
        cursor.execute("""
            INSERT INTO vacancies (id, title, salary_from, salary_to, experience, published_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (hh_vacancy_id, vacancy_title, salary_from, salary_to, experience_requirements, date_of_publish))

    connection.commit()  # Сохраняем изменения в базе данных
    cursor.close()  # Закрываем курсор
    connection.close()  # Закрываем соединение

# Функция для загрузки новых данных в базу данных
def load_daily_data_to_db():
    # Обозначим период, за который требуется загрузка в формате YYYY-MM-DD  
    start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') 
    end_date = start_date

    # Извлекаем данные за указанный период
    vacancies = extract_data_from_api(start_date, end_date)

    # Подключаемся к базе данных PostgreSQL
    connection = psycopg2.connect(
        dbname='hh_data_engineer',
        user='worker',
        password='password',
        host='localhost',
        port='5432'  
    )
    cursor = connection.cursor()

    for item in vacancies:  # Извлекаем список вакансий
        # Извлекаем необходимые данные о вакансии
        hh_vacancy_id = item.get("id")  # ID вакансии с сайта hh.ru
        vacancy_title = item.get("name")[:50] if item.get("name") else None  # Название вакансии
        salary = item.get("salary")
        salary_from = salary.get("from") if salary else None  # Минимальная зарплата
        salary_to = salary.get("to") if salary else None  # Максимальная зарплата
        experience = item.get("experience") 
        experience_requirements = experience.get("name") if experience else None  # Требования к опыту работы
        date_of_publish = item.get("published_at")  # Дата публикации вакансии
  
        # Выполним преобразование date_of_publish в формат DATE
        if date_of_publish:
            # Приведение к объекту date
            date_of_publish = datetime.strptime(date_of_publish, "%Y-%m-%dT%H:%M:%S%z").date()

        # Вставляем данные в таблицу vacancies в базе данных PostgreSQL
        cursor.execute("""
            INSERT INTO vacancies (id, title, salary_from, salary_to, experience, published_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (hh_vacancy_id, vacancy_title, salary_from, salary_to, experience_requirements, date_of_publish))

    connection.commit()  # Сохраняем изменения в базе данных
    cursor.close()  # Закрываем курсор
    connection.close()  # Закрываем соединение

# Задача для создания таблицы для сохранения извлеченных данных
create_table_task = PythonOperator(
    task_id="create_table_vacancies",
    python_callable=create_table_vacancies,
    dag=dag
)

# Задача для извлечения исторических данных
load_historical_data_task = PythonOperator(
    task_id='load_historical_data_to_db',
    python_callable=load_historical_data_to_db,
    dag=dag,
)

# Задача для загрузки данных каждый день
load_daily_data_task = PythonOperator(
    task_id='load_daily_data_to_db',
    python_callable=load_daily_data_to_db,
    dag=dag,
)

# Определение зависимостей
create_table_task >> load_historical_data_task >> load_daily_data_task

