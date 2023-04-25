import sqlite3
from datetime import datetime

# Константа с именем базы данных для удобства
DB_NAME = 'Profile.db'


if __name__ == '__main__':
    """
    - Создаем базу данных Profile
    - Создаем таблицу Cookie Profile:
    * Уникальной id для каждой строки (Not NULL)
    * Дата и время создания записи (Not NULL)
    * Значения Cookie
    * Дата и время последнего запуска
    * Кол-во всего запусков
    - Заполняем таблицу 15 значениями (id, текущая дата и время создания)
    """
    # Создаем базу данных "Profile"
    conn = sqlite3.connect(DB_NAME)

    # Создание таблицы "Cookie_Profile"
    conn.execute('''CREATE TABLE IF NOT EXISTS Cookie_Profile
             (ID INTEGER PRIMARY KEY NOT NULL,
             COOKIE_VALUE TEXT DEFAULT NULL,
             CREATED_AT TIMESTAMP NOT NULL,
             RUN_COUNT INTEGER DEFAULT "0",
             LAST_RUN TIMESTAMP DEFAULT NULL
             );''')

    # Заполняем таблицу 15 пустыми значениями (текущее время создания)
    for i in range(15):
        now = datetime.now()
        conn.execute(f"INSERT INTO Cookie_Profile (CREATED_AT) VALUES ('{now}')")

    conn.commit()  # Выполняем
    conn.close()  # Закрываем соединение
