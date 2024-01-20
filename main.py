# Сбор и разметка данных (семинары)
# Урок 7. Selenium в Python
# Задание

# 1. Выберите веб-сайт, который содержит информацию, представляющую интерес для извлечения данных. Это может
#    быть новостной сайт, платформа для электронной коммерции или любой другой сайт, который позволяет осуществлять
#    скрейпинг (убедитесь в соблюдении условий обслуживания сайта).
# 2. Используя Selenium, напишите сценарий для автоматизации процесса перехода на нужную страницу сайта.
# 3. Определите элементы HTML, содержащие информацию, которую вы хотите извлечь (например, заголовки статей, названия
#    продуктов, цены и т.д.).
# 4. Используйте BeautifulSoup для парсинга содержимого HTML и извлечения нужной информации из идентифицированных
#    элементов.
# 5. Обработайте любые ошибки или исключения, которые могут возникнуть в процессе скрейпинга.
# 6. Протестируйте свой скрипт на различных сценариях, чтобы убедиться, что он точно извлекает нужные данные.
# 7. Предоставьте ваш Python-скрипт вместе с кратким отчетом (не более 1 страницы), который включает следующее:
#    - URL сайта. Укажите URL сайта, который вы выбрали для анализа.
#    - Описание. Предоставьте краткое описание информации, которую вы хотели извлечь из сайта.
#    - Подход. Объясните подход, который вы использовали для навигации по сайту, определения соответствующих
#      элементов и извлечения нужных данных.
#    - Трудности. Опишите все проблемы и препятствия, с которыми вы столкнулись в ходе реализации проекта,
#      и как вы их преодолели.
#    - Результаты. Включите образец извлеченных данных в выбранном вами структурированном формате
#      (например, CSV или JSON).
#
# Примечание: Обязательно соблюдайте условия обслуживания сайта и избегайте чрезмерного скрейпинга, который
# может нарушить нормальную работу сайта.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import re
import csv

TARGET_URL = 'https://www.litres.ru/'
SEARCH_STR = 'Булгаков'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'


def book_data(book_url):
    data = {'Author': None,
            'Name': None,
            'Format': None,
            'Price': None,
            'Rating': None,
            'Url': book_url,
            }
    response = requests.get(book_url, headers={'User-Agent': user_agent})
    page = BeautifulSoup(response.text, 'html.parser')
    try:
        data['Name'] = page.find(class_='BookCard-module__book__mainInfo__title_2zz4M').text
    except ValueError:
        pass
    except AttributeError:
        pass
    try:
        data['Format'] = page.find(class_='Label-module__formatText_3pNcK').text
    except ValueError:
        pass
    except AttributeError:
        pass
    try:
        data['Price'] = float(re.findall(r'\b\d+(?:.\d+)?',
                                         page.find(class_='SaleBlock-module__block__price__default_kE68R').text)[0])
    except ValueError:
        pass
    except AttributeError:
        pass
    try:
        data['Rating'] = float(re.findall(r'\b\d+(?:.\d+)?',
                                          page.find(class_='BookFactoids-module__primary_kvfPy').text
                                          .replace(',', '.'))[0])
    except ValueError:
        pass
    except AttributeError:
        pass
    try:
        data['Author'] = "; ".join([author.text for author in  # Если вдруг авторов несколько
                                    page.find(class_='Authors-module__authors__wrapper_1rZey').find_all('span')])
    except ValueError:
        pass
    except AttributeError:
        pass
    return data


def my_save_to_csv(filename, local_data):
    """
    Записываем список из словарей local_data в CSV-файл filename
    :param filename: Путь к файлу для записи
    :param local_data: Список из словарей с данными
    :return:
    """
    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Author', 'Name', 'Format', 'Price', 'Rating', 'Url'])  # Пишем заголовок
        for row in local_data:
            writer.writerow(row.values())


if __name__ == '__main__':

    print('Начало работы')
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    # Запускаем браузер
    driver = webdriver.Chrome(options=options)
    driver.get(TARGET_URL)
    # Задаем поиск
    search_box = driver.find_element(By.CLASS_NAME, 'SearchForm-module__input_2AIbu')
    search_box.send_keys(SEARCH_STR)
    search_box.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

    scroll_pause_time = 2
    last_height = driver.execute_script('return document.documentElement.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight - 10);')
        time.sleep(scroll_pause_time)
        print(f'скроллинг идет!')

        #        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

    books_links = driver.find_elements(By.XPATH, '//a[@class="AdaptiveCover-module_'
                                                 '_container_1j6Nv AdaptiveCover-module__container__pointer_vavb5"]')
    print(f'Найдено {len(books_links)} ссылок')
    # result = [book_data(url.get_attribute('href')) for url in tqdm(books_links,'Обработка найденных книг')]
    # my_save_to_csv('litres.csv', result)
    driver.quit()
    print('Работа завершена.')
