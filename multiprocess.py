from selenium import webdriver
import random
import sqlite3
from datetime import datetime
import time
from sql import DB_NAME
from my_requests import LINKS


def process_profile(profile_id: int) -> None:
    """
    - Создаем сессию (имеющиеся Cookie, добавляем сессии)
    - Переходим по рандомной ссылке из массива модуля Requests
    - Прокручиваем страницу с рандомной задержкой
    - Сохраняем Cookie в SQLite (обновляем значения профиля)
    - Закрываем сессию
    """
    # Получаем Cookie для профиля из базы данных SQLite
    print('starting processing -----------------')
    _conn = sqlite3.connect(DB_NAME)
    _c = _conn.cursor()
    _c.execute(f"SELECT Cookie_value FROM Cookie_Profile WHERE id={profile_id};")
    cookie = _c.fetchone()[0]
    _conn.close()
    # Создаем экземпляр драйвера Selenium и передаем ему Cookie
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir=./user_data_{profile_id}")
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--cookie="{cookie}"')
    driver = webdriver.Chrome(options=options)
    random_link = random.choice(LINKS)
    driver.get(random_link)

    # Прокручиваем страницу с рандомной задержкой
    scroll_amount = random.randint(1, 3)
    for i in range(scroll_amount):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(1, 3))

    # Сохраняем Cookie в SQLite (обновляем значения профиля)
    new_cookie = driver.get_cookies()
    _conn = sqlite3.connect(DB_NAME)
    _c = _conn.cursor()
    _c.execute(f'UPDATE Cookie_Profile SET Cookie_value="{new_cookie}",\
                                    Last_Run="{datetime.now()}",\
                                    Run_Count=Run_Count+1\
                                        WHERE id={profile_id};')
    _conn.commit()
    _conn.close()

    # Закрываем сессию
    driver.quit()
    print('------------------- ending processing')


# Получаем список профилей из базы данных SQLite
def profiles() -> list:
    """
    - Собираем профиля из таблицы Cookie Profile(-> Cookies) (кол-во процессов)
    """
    conn2 = sqlite3.connect(DB_NAME)
    c2 = conn2.cursor()
    c2.execute("SELECT ID FROM 'Cookie_Profile';")  # Собираем все имеющиеся профили в нашей бд
    profile_ids = [x[0] for x in c2.fetchall()]  # Записываем их ID в список
    conn2.close()
    return profile_ids

