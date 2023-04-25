from multiprocess import process_profile, profiles
from multiprocessing import Pool

# Перекладываем профиля в переменную
profiles = profiles()

if __name__ == '__main__':
    """
    - Используем Pool для создания процессов на каждый профиль
    - Ограничение 5 одновременных процессов
    """
    with Pool(processes=5) as pool:
        # 'processes=5' - ограничение на 5 одновременных процессов
        pool.map(process_profile, profiles)  # Передаем каждый ID в функцию process_profile
