class DBManager:

    @staticmethod
    def get_companies_and_vacancies_count(cur) -> list[tuple]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :param cur: Объект cursor для выполнения запросов.
        :return: Список кортежей с информацией из БД.
        """
        cur.execute('SELECT employer_name, vacancies_count FROM employers')
        raw: list[tuple] = cur.fetchall()
        return raw

    @staticmethod
    def get_all_vacancies(cur) -> list[tuple]:
        """
        Получает список всех вакансий с указанием:
        названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :param cur: Объект cursor для выполнения запросов.
        :return: Список кортежей с информацией из БД.
        """
        cur.execute("""
            SELECT employers.employer_name, vacancy_name, salary_from, salary_to, salary_currency,vacancies_url
            FROM vacancies
            INNER JOIN employers USING (employer_id) 
        """)
        raw: list[tuple] = cur.fetchall()
        return raw

    @staticmethod
    def get_avg_salary(cur) -> list[tuple]:
        """
        Получает среднюю зарплату по вакансиям.
        :param cur: Объект cursor для выполнения запросов.
        :return: Список кортежей с информацией из БД.
        """
        cur.execute("""
                    SELECT ROUND(AVG((salary_from + salary_to) / 2), 2)
                    FROM vacancies
                """)
        raw: list[tuple] = cur.fetchall()
        return raw

    @staticmethod
    def get_vacancies_with_higher_salary(cur) -> list[tuple]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :param cur: Объект cursor для выполнения запросов.
        :return: Список кортежей с информацией из БД.
        """
        cur.execute("""
                    SELECT *
                    FROM vacancies
                    WHERE ((salary_from + salary_to) / 2) > (SELECT ROUND(AVG((salary_from + salary_to) / 2), 2)
                    FROM vacancies)
                """)
        raw: list[tuple] = cur.fetchall()
        return raw

    @staticmethod
    def get_vacancies_with_keyword(cur, key_word: str) -> list[tuple]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        :param cur: Объект cursor для выполнения запросов.
        :param key_word: Ключевое слово для запроса.
        :return: Список кортежей с информацией из БД.
        """
        cur.execute("""
                    SELECT *
                    FROM vacancies
                    WHERE LOWER(vacancy_name) LIKE LOWER(%s)
                """, ('%' + key_word + '%',))
        raw: list[tuple] = cur.fetchall()
        return raw
