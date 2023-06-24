import json
from abc import ABC, abstractmethod
import requests
import os


class JobAPI(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(JobAPI):
    url = "https://api.hh.ru/vacancies"

    def __init__(self, keyword):
        self.params = {
            "per_page": 100,
            "page": 1,
            "text": keyword,
            "archived": False
        }
        self.headers = {
            "User-Agent": "MyImportantApp 1.0"
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        return response.json()["items"]

    def get_vacancies(self, pages_count=1):
        """Получение списка вакансий с сайта HeadHunter"""
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            page_vacancies = self.get_request()
            self.vacancies.extend(page_vacancies)
            print(f"Загружено {len(page_vacancies)} вакансий")

    def get_form_vacancies(self):
        """Приведение списка вакансий к единому формату"""
        form_vacancies = []
        for vacancy in self.vacancies:
            form_vacancy = {
                "employer": vacancy["employer"]["name"],
                "title": vacancy["name"],
                "url": vacancy["alternate_url"],
                "api": "HeadHunter",
            }
            salary = vacancy["salary"]
            if salary:
                form_vacancy["salary_from"] = salary["from"]
                form_vacancy["salary_to"] = salary["to"]
                form_vacancy["currency"] = salary["currency"]
            else:
                form_vacancy["salary_from"] = None
                form_vacancy["salary_to"] = None
                form_vacancy["currency"] = None
            form_vacancies.append(form_vacancy)
        return form_vacancies


class SuperJobAPI(JobAPI):
    url = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, keyword):
        self.params = {
            "per_page": 100,
            "page": None,
            "text": keyword,
            "archived": False
        }
        self.headers = {
            "X-Api-App-Id": os.getenv('JOB_API')
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        return response.json()["objects"]

    def get_vacancies(self, pages_count=1):
        """Получение списка вакансий с сайта SuperJob"""
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            page_vacancies = self.get_request()
            self.vacancies.extend(page_vacancies)
            print(f"Загружено {len(page_vacancies)} вакансий")

    def get_form_vacancies(self):
        """Приведение списка вакансий к единому формату"""
        form_vacancies = []
        for vacancy in self.vacancies:
            form_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "api": "SuperJob",
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy["payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None,
                "currency": vacancy["currency"]
            }
            form_vacancies.append(form_vacancy)
        return form_vacancies


class Vacancy:
    """Создание класса для работы с вакансиями"""
    def __init__(self, vacancy):
        self.employer = vacancy["employer"]
        self.title = vacancy["title"]
        self.url = vacancy["url"]
        self.api = vacancy["api"]
        self.salary_from = vacancy["salary_from"]
        self.salary_to = vacancy["salary_to"]
        self.currency = vacancy["currency"]

    def __str__(self):
        if not self.salary_from and not self.salary_to:
            salary = "Не указана"
        else:
            salary_from, salary_to = "", ""
            if self.salary_from:
                salary_from = f"от {self.salary_from} {self.currency}"
            if self.salary_to:
                salary_to = f"до {self.salary_to} {self.currency}"
            salary = " ".join([salary_from, salary_to]).strip()
        return f"""
Работодатель: \"{self.employer}\"
Вакансия: \"{self.title}\"
Зарплата: {salary}
Ссылка: {self.url}
        """


class JSONSaver:
    """Создание класса для сохранения и фильтров вакансий"""
    def __init__(self, keyword, vacancies_json):
        self.filename = f"{keyword}.json"
        self.add_vacancy(vacancies_json)

    def add_vacancy(self, vacancies_json):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_json, file, indent=4)

    def select(self):
        """Вывести список вакансий"""
        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [Vacancy(x) for x in vacancies]

    def get_vacancies_by_salary(self):
        """Сортировка по мин. зарплате"""
        desc = True if input(
            "> - DESC \n"
            "< - ASC \n>>> "
        ).lower() == ">" else False
        vacancies = self.select()
        return sorted(vacancies, key=lambda x: (x.salary_from if x.salary_from else 0, x.salary_to if x.salary_to else 0), reverse=desc)

    def filter_vacancies(self, filter_words):
        """Сортировка по ключевому слову"""
        filtered_vacancies = []
        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
            for vacancy in vacancies:
                if filter_words in vacancy['title']:
                    filtered_vacancies.append(vacancy)
        if not filtered_vacancies:
            print("Нет вакансий, соответствующих заданным критериям.")
        return [Vacancy(x) for x in filtered_vacancies]
