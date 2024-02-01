from classes import Superjob, HeadHunter
from json_saver import JSONSaver
from vacancy import Vacancy


def print_vacancies(vacancies):
    """
    Выводит информацию о вакансиях в консоль.
    """
    for vacancy in vacancies:
        print(f"{'Название вакансии:':<30} {vacancy.name}")
        print(f"{'Ссылка:':<30} {vacancy.url}")
        print(f"{'Зарплата:':<30} {vacancy.salary_from} to {vacancy.salary_to}")
        print(f"{'Описание:':<30} {vacancy.description}")
        print("-" * 50)


def user_integration():
    """
    Основная функция для взаимодействия с пользователем и выполнения поиска вакансий.
    """
    global selected_platform
    platform_choice = input("""Выберите платформу для поиска вакансий:
1 - HeadHunter
2 - SuperJob
3 - Поиск по обеим платформам
""")
    search_query = input("Введите поисковый запрос: ")
    hh = HeadHunter()
    superjob = Superjob()
    hh_vacancies = hh.filter_vacancies(search_query)
    superjob_vacancies = superjob.filter_vacancies(search_query)

    if platform_choice == "1":
        selected_platform = hh_vacancies
        print("Выбрана платформа HeadHunter")
    elif platform_choice == "2":
        selected_platform = superjob_vacancies
        print("Выбрана платформа SuperJob")
    elif platform_choice == "3":
        selected_platform = hh_vacancies + superjob_vacancies
        print("Выбраны обе платформы")

    selected_platform = [Vacancy(v["name"], v["url"], v["salary_from"], v["salary_to"], v["description"]) for v in
                         selected_platform]

    json_saver = JSONSaver("test.json")
    json_saver.save_vacancies(selected_platform)

    choice = input("Введите 1 для вывода всех вакансий, 2 для сортировки по зарплате, 3 для топ-N: ")

    if choice == "1":
        print_vacancies(selected_platform)
    elif choice == "2":
        min_salary = float(input("Введите минимальную зарплату (нажмите Enter, чтобы пропустить): ") or 0)
        max_salary = float(input("Введите максимальную зарплату (нажмите Enter, чтобы пропустить): ") or float('inf'))
        json_saver = JSONSaver("test.json")
        filtered_by_salary = json_saver.filter_vacancies_by_salary(min_salary, max_salary)
        print_vacancies(filtered_by_salary)
    elif choice == "3":
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        top_vacancies = sorted(selected_platform, key=lambda x: (x.salary_from or 0), reverse=True)[:top_n]
        print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_integration()

