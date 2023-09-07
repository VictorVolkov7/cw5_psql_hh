import os

import requests

from src.db_manager import DBManager


def exchange_rates(currency: str) -> float:
    """
    Получает данные о зарплате и переводит по курсу в рубли, используя API exchangerates
    :param currency: Валюта для поиска курса в рублях
    :return: Курс в рублях
    """
    api_key = os.getenv('ER_API_KEY')
    params = {
        'base': currency,
        'symbols': 'RUB'
    }
    headers = {'apikey': api_key}
    try:
        response = requests.get('https://api.apilayer.com/exchangerates_data/latest',
                                headers=headers, params=params).json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ReadTimeout as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError as err:
        raise SystemExit(err)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    return response['rates']['RUB']


def welcome(cur):
    """
    Пользовательский интерфейс, возвращает метод класса DBManager
    для осуществления запроса.
    :param cur: Объект cursor для выполнения запросов.
    :return: Класса DBManager.
    """
    db_manager = DBManager()
    user_interface_dict: dict = {
        1: db_manager.get_companies_and_vacancies_count,
        2: db_manager.get_all_vacancies,
        3: db_manager.get_avg_salary,
        4: db_manager.get_vacancies_with_higher_salary,
        5: db_manager.get_vacancies_with_keyword,
        6: 'Завершить работу программы'
    }
    while True:
        try:
            user_input: int = int(input("""Здравствуйте, выберите цифрой один и предложенных вам запросов:
                                \r1 - Получить список всех компаний и количество вакансий
                                \r2 - Получить список всех вакансий с указанием компании
                                \r3 - Получить среднюю зарплату по вакансиям
                                \r4 - Получить список вакансий, у которых зарплата выше средней по вакансиям
                                \r5 - Получить список всех вакансий по ключевому слову
                                \r6 - Завершить работу программы\n"""))

            if user_input == 6:
                break
            elif user_input in [1, 2, 3, 4]:
                return user_interface_dict[user_input](cur)
            elif user_input == 5:
                return user_interface_dict[user_input](cur, input('Введите ключевое слово: '))
            else:
                print('Введенного значения не существует. Попробуйте снова...\n')

        except ValueError:
            print("Пожалуйста, введите число от 1 до 6.\n")


def user_answer_check(massage: str):
    """
    Функция, которая принимает какое-то сообщение и служит для повторной реализации какого то кода,
    возвращает boll и брейкует циклы while True
    :param massage:
    :return: bool
    """
    while True:
        user_input: str = input(massage).lower()
        if user_input in ['да', 'yes']:
            return True
        elif user_input in ['нет', 'no']:
            return False
        else:
            print('Не понял вас, повторите ещё.')
