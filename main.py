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




TARGET_URL = 'https://www.litres.ru/'

if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ' \
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    options = Options()
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=options)
    driver.get(TARGET_URL)

    search_box = driver.find_element(By.CLASS_NAME, 'SearchForm-module__input_2AIbu')
#    search_box = driver.find_element(By.XPATH, '//form[input/@class ="c1vr6imw_main_page"]')

    search_box.send_keys("Булгаков")
    search_box.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

    # iframe = driver.find_element(By.CLASS_NAME, 'Button-module__textContainer_1I67-')
    # ActionChains(driver) \
    #     .scroll_to_element(iframe) \
    #     .perform()
    scroll_pause_time = 2
    last_height = driver.execute_script('return document.documentElement.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
        time.sleep(scroll_pause_time)
        print(f'скроллинг идет!')

        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        last_height = new_height    # УБРАТЬ!!!!!!!!

        if new_height == last_height:
            break

        last_height = new_height

    books_links = driver.find_elements(By.XPATH, '//a[@class="AdaptiveCover-module__container_1j6Nv AdaptiveCover-module__container__pointer_vavb5"]')

    print('======================')
    for url in books_links:
        print(url.get_attribute('href'))
    print('======================')

    driver.quit()
