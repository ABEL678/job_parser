from classes import HeadHunterAPI, SuperJobAPI, JSONSaver


def main():
    keyword = input("Введите поисковый запрос: ")
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI(keyword)
    sj_api = SuperJobAPI(keyword)

    # Получение вакансий с разных платформ
    vacancies_json = []
    for api in (hh_api, sj_api):
        api.get_vacancies(pages_count=5)
        vacancies_json.extend(api.get_form_vacancies())

    json_saver = JSONSaver(keyword=keyword, vacancies_json=vacancies_json)
    # Создание экземпляра класса для работы с вакансиями
    # vacancy = Vacancy("Python Developer")
    #
    # # Сохранение информации о вакансиях в файл
    # json_saver = JSONSaver()
    # json_saver.add_vacancy(vacancy)
    # json_saver.get_vacancies_by_salary("100 000-150 000 руб.")
    # json_saver.delete_vacancy(vacancy)
    # search_query = input("Введите поисковый запрос: ")
    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    # filtered_vacancies = filter_vacancies(filter_words)
    #
    # if not filtered_vacancies:
    #     print("Нет вакансий, соответствующих заданным критериям.")
    #     return
    #
    # sorted_vacancies = sort_vacancies(filtered_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)

    while True:
        vacancies = []
        command = input(
            "1 - Вывести список вакансий; \n"
            "2 - Сортировка по мин. зарплате; \n"
            "3 - Сортировка по ключевому слову; \n"
            "exit - выход. \n"
            ">>> "
        )
        if command.lower() == "exit":
            break
        elif command == "1":
            vacancies = json_saver.select()
        elif command == "2":
            vacancies = json_saver.get_vacancies_by_salary()
        elif command == "3":
            filter_words = input("Введите ключевые слова для фильтрации вакансий: ")
            vacancies = json_saver.filter_vacancies(filter_words)
        for vacancy in vacancies:
            print(vacancy, end='\n')


# Функция для взаимодействия с пользователем
# def user_interaction():
#     platforms = ["HeadHunter", "SuperJob"]
#     search_query = input("Введите поисковый запрос: ")
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)
#
#     if not filtered_vacancies:
#         print("Нет вакансий, соответствующих заданным критериям.")
#         return
#
#     sorted_vacancies = sort_vacancies(filtered_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)


if __name__ == "__main__":
    main()
    # user_interaction()
