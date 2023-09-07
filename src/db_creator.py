import psycopg2


class DBCreator:
    """
    Класс для работы с базой данных PostgreSQL.
    """

    def __init__(self, database_name: str):
        """
        Инициализатор класса DBCreator.
        :param database_name: Название базы данных для подключения.
        """
        self.database_name: str = database_name

    def creating_database(self, db_name: str, params: dict) -> None:
        """
        Создание базы данных для последующей работы с ней.
        """
        conn = psycopg2.connect(dbname=self.database_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            # Проверяет существование базы данных, и если существует, удаляет её
            cur.execute(f"SELECT datname FROM pg_database WHERE datname = '{db_name}'")
            database_exists = cur.fetchone()
            if database_exists:
                cur.execute(f"DROP DATABASE {db_name}")

            cur.execute(f'CREATE DATABASE {db_name}')

        conn.close()

    @staticmethod
    def creating_tables(cur) -> None:
        """
        Подключение к БД и создание таблиц.
        :param cur: Объект cursor для выполнения запросов.
        """
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY, 
                employer_name VARCHAR(50),
                vacancies_count INTEGER,
                employer_url VARCHAR(50)
            )
        """)

        cur.execute("""
            CREATE TABLE vacancies (
                employer_id INTEGER,
                vacancy_name TEXT NOT NULL,
                city VARCHAR(50),
                salary_from INTEGER NOT NULL,
                salary_to  INTEGER NOT NULL,
                salary_currency VARCHAR(5) NOT NULL,
                vacancies_url VARCHAR(50) NOT NULL,
                
                CONSTRAINT fk_vacancies_employer_id FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
            )
        """)

    @staticmethod
    def filling_db(emp_data: list[dict], vac_data: list[dict], cur) -> None:
        """
        Заполнение БД данными.
        :param emp_data: Данные для заполнения таблицы employers.
        :param vac_data: Данные для заполнения таблицы vacancies.
        :param cur: Объект cursor для выполнения запросов.
        """
        for info in emp_data:
            cur.execute(
                f"""
                INSERT INTO employers (employer_name, vacancies_count, employer_url)
                VALUES (%s, %s, %s)""", tuple(info.values())
            )

        for info in vac_data:
            cur.execute(
                f"""
                INSERT INTO vacancies(employer_id, vacancy_name, city, salary_from, salary_to, salary_currency, 
                vacancies_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""", tuple(info.values())
            )
