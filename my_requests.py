import requests
from bs4 import BeautifulSoup

# - GET запросом получаем содержимое страницы (https://news.google.com/home)
params = dict(hl='ru', gl='ru')  # Доп.параметры выбора региона запроса в google (Ru)
# GET запрос на указанный адрес с выбранными параметрами
response = requests.get('https://news.google.com/home', params=params)


def get_new_links() -> list or 0:
    """
    Получение списка ссылок из google news.
     - Собираем в массив, ссылки на новости
    """
    # Успешность запроса
    if response.status_code == 200:
        # Если запрос успешен, получаем содержимое страницы в формате текста
        content = response.text
        # Создаем объект BeautifulSoup
        b_soup = BeautifulSoup(content, 'html.parser')
        # Находим все ссылки на новости на странице
        news_links = []
        # Ищем все <a> на странице с классом, подходящим для новостей
        for link in b_soup.find_all('a', class_='WwrzSb'):
            f_link = link['href'][1:]  # Первый символ в ссылке "." (точка), которую уберем и заменим на url ниже
            news_links.append(f'https://news.google.com{f_link}')  # Добавляем готовую ссылку в лист
        return news_links

    else:
        # Если запрос неуспешен, выводим соответствующее сообщение об ошибке
        print('Error:', response.status_code)
        return 0


LINKS = get_new_links()
