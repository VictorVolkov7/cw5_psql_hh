import psycopg2

from settings import DATABASE_INI_PATH
from src.api_hh_parser import HeadHuntersAPI
from src.config import config
from src.db_creator import DBCreator
from src.utils import welcome, user_answer_check


def main():
    # Получаем информацию о работодателях и их вакансиях
    employers_for_hh = HeadHuntersAPI()
    emp_data: list[dict] = employers_for_hh.get_employers_info
    vac_data: list[dict] = employers_for_hh.get_vacancies_info

    # Создание БД, подключение к ней
    db_name = 'hh_parser'
    params = config(DATABASE_INI_PATH)
    creator_db = DBCreator('postgres')
    creator_db.creating_database(db_name, params)
    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                # Создание таблиц БД
                creator_db.creating_tables(cur)
                # Заполнение БД данными
                creator_db.filling_db(emp_data, vac_data, cur)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    # Подключение к базе данных
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            # Работа с пользователем
            interface = True
            try:
                while interface:
                    data: list[tuple] = welcome(cur)
                    for info in data:
                        print(info)

                    # Проверка после выполненного запроса
                    if not user_answer_check('Хотите выбрать другие фильтры? (да/нет): \n'):
                        print('Всего доброго, до скорых встреч!')
                        interface = False

            except TypeError:
                print('Всего доброго, увидимся позже!\n')


if __name__ == '__main__':
    main()
