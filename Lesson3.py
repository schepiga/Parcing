import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from pprint import pprint


def _parser_hh(job):
    url = 'https://hh.ru'
    params = {'clusters': 'true',
              'area': '1',
              'ored_clusters': 'true',
              'enable_snippets': 'true',
              'salary': 'None',
              'st': 'searchVacancy',
              'text': job
              }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = bs(response.text, 'html.parser')

    all_vacancies = []

    while True:
        vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})
        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('a').getText()
            vacancy_link = vacancy.find('a')['href']
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            salary_min = None
            salary_max = None
            salary_curr = None
            if vacancy_salary is not None:
                vacancy_salary = vacancy_salary.getText().replace('\u202f', '')
                salary_curr = vacancy_salary.split()[-1]
                if vacancy_salary.find('–') > -1:
                    salary_min = int(vacancy_salary.split()[0])
                    salary_max = int(vacancy_salary.split()[2])
                elif vacancy_salary.find('от'):
                    salary_min = int(vacancy_salary.split()[1])
                elif vacancy_salary.find('до'):
                    salary_max = int(vacancy_salary.split()[1])

            vacancy_data['name'] = vacancy_name
            vacancy_data['url'] = vacancy_link
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_curr'] = salary_curr
            all_vacancies.append(vacancy_data)

        next_button = dom.find('a', {'data-qa': 'pager-next'})

        if next_button is None:
            break
        else:
            next_link = url + next_button['href']
            response = requests.get(next_link, headers=headers)
            dom = bs(response.text, 'html.parser')

    return all_vacancies


client = MongoClient('localhost', 27017)
db = client['hh_vacancies_db']
collection = db.hh_vacancies_collestion
collection.insert_many(_parser_hh('pilot'))


def find_salary_limit(salary_limit):
    for vacancy in collection.find({'$or': [{'salary_min': {'$gt': salary_limit}},
                                            {'salary_max': {'$gt': salary_limit}}]}):
        pprint(vacancy)


def find_new_vacancies(new_vacancy):
    url = 'https://hh.ru'
    params = {'clusters': 'true',
              'area': '1',
              'ored_clusters': 'true',
              'enable_snippets': 'true',
              'salary': 'None',
              'st': 'searchVacancy',
              'text': 'new_vacancy'
              }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = bs(response.text, 'html.parser')

    vacancy = dom.find('a')
    for item in collection.update_one({'url': vacancy['href']}, {'$set': vacancy}, upsert=True):
        pprint(item)


# print(find_salary_limit(100000))
# print(find_new_vacancies('pilot'))
