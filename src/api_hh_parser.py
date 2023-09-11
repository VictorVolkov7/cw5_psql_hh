import requests

from src.utils import exchange_rates


class HeadHuntersAPI:
    """
    Класс для работы с API HeadHunters
    """
    employers_id: list = [52389, 882, 1122462, 64174, 127256, 78638, 15478, 2180, 1740, 852361]  # id работодателей
    currency_dict: dict = {}  # Список валют

    @property
    def get_employers_info(self) -> list[dict]:
        """
        Получение информации о работодателях с API HH.
        :return: employers_info - список со словарями о работодателях.
        """
        employers_info: list = []

        try:
            for employer in HeadHuntersAPI.employers_id:
                request = requests.get(f'https://api.hh.ru/employers/{employer}').json()
                # для последующей удобной работы с таблицами бд
                employers_info.append({
                    'employer_name': request['name'],
                    'vacancies_count': request['open_vacancies'],
                    'employer_url': request['alternate_url']
                })
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.ReadTimeout as err:
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        return employers_info

    @property
    def get_vacancies_info(self) -> list[dict]:
        """
        Получение информации о вакансиях, используя id работодателя.
        :return: Список со словарями с информацией о вакансиях.
        """
        vacancies_info: list = []
        try:
            for num, employer in enumerate(HeadHuntersAPI.employers_id):
                for page in range(0, 1):
                    params: dict = {
                        'employer_id': employer,  # ID работодателя
                        'page': page,  # Номер страницы
                        'per_page': 10  # Кол-во вакансий на 1 странице
                    }
                    for vac in (requests.get('https://api.hh.ru/vacancies', params=params).json()['items']):
                        # Для последующей удобной работы с таблицами бд
                        salary_from, salary_to, salary_currency = 0, 0, 'RUB'

                        # Проверка данных о ЗП и перевод в рубли
                        if vac['salary'] is None:
                            salary_from, salary_to, salary_currency = 0, 0, 'RUB'
                        else:
                            s_from: int = vac['salary'].get('from') or 0
                            s_to: int = vac['salary'].get('to') or 0
                            s_currency: str = 'RUB' if vac['salary']['currency'] == 'RUR' else vac['salary']['currency']
                            salary_from, salary_to, salary_currency = self.calc_salary(s_from, s_to, s_currency)

                        vacancies_info.append({
                            'employer_id': num + 1,
                            'vacancy_name': vac['name'],
                            'city': 'Город не указана' if vac['area'] is None else vac['area']['name'],
                            'salary_from': salary_from,
                            'salary_to': salary_to,
                            'salary_currency': salary_currency,
                            'vacancies_url': vac['alternate_url']
                        })
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.ReadTimeout as err:
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        return vacancies_info

    @staticmethod
    def calc_salary(salary_from: int, salary_to: int, salary_currency: str) -> tuple:
        """
        Принимает минимальную и предельную зарплату, переводит по курсу валют.
        Полученные курсы валют сохраняются в словаре и переиспользуются,
        чтобы не обращаться большое количество раз к API
        """
        if salary_currency not in HeadHuntersAPI.currency_dict:
            factor: float = exchange_rates(salary_currency)
            HeadHuntersAPI.currency_dict[salary_currency] = factor

        salary_from *= HeadHuntersAPI.currency_dict[salary_currency]
        salary_to *= HeadHuntersAPI.currency_dict[salary_currency]
        salary_currency: str = 'RUB'

        return round(salary_from), round(salary_to), salary_currency
