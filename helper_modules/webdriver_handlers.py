"""
    Файл с функциями для обработки и взаимодействия с браузеорм
"""

# Модуль os в Python предоставляет функции для взаимодействия с операционной системой.
import os

# Модуль os в Python предоставляет функции для взаимодействия с операционной системой.
import time

# Модуль для явного указания типов данных
from typing import NoReturn
from typing import List,Dict


# Модули Selenium
# Класс webdriver нужен для инициализации бразуера
from selenium import webdriver
# Класс для поиска элементов на страничке (по классам, id и т.д.)
from selenium.webdriver.common.by import By
# Исключение Selenium которое вызывается при не нахождении элемента
from selenium.common.exceptions import NoSuchElementException
# Service нужен для конфигурации и запуска экземпляра webdriver(браузер)
from selenium.webdriver.firefox.service import Service

# Вспомогательные функции
# Функция для сбора информации о первом элементе с странички Avito
from parser_modules.parser_avito import parse_first_add_avito
# Исключение для обработки ошибок WebDriver
from helper_modules.exeptions import WebDriverExeption
# Валидатор данных объявления
from helper_modules.validators import ad_data_validator
# Функция для красивого вывода данных
from helper_modules.output_data_handlers import beautiful_info_cmd


def scroll_down(passed_in_driver: webdriver.Firefox) -> NoReturn:  # type: ignore
    """
        Функция для скролла странички вниз на 200px
    """
    scroll_nav_out_of_way: str = 'window.scrollBy(0, 200);'
    passed_in_driver.execute_script(scroll_nav_out_of_way)

def initial_browser() -> webdriver.Firefox:
    """
        Функция для инициализации браузера
        Возвращает экземпляр webdriver в котором
        открыты все нужные ссыллки авито
    """
    install_dir: str = ".\\additional_tools\\Mozilla Firefox\\"
    driver_loc: str = os.path.join(install_dir, "geckodriver")
    binary_loc: str = os.path.join(install_dir, "firefox.exe")

    service: Service = Service(driver_loc)

    opts: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
    opts.set_preference('dom.webdriver.enabled', False)
    opts.add_argument('-headless')
    opts.binary_location = binary_loc
    opts.set_preference("log.level", "OFF")
    opts.page_load_strategy = 'eager'

    browser: webdriver.Firefox = webdriver.Firefox(
        service=service, options=opts)

    return browser
# pylint: disable=line-too-long
def initial_start(avito_links: List[str], cian_link: str) -> NoReturn:# type: ignore
    """
        Функция для старта всего сервиса
        Собирает все модули в одном месте и управляет ими
    """
# pylint: enable=line-too-long
    # Массив для объявлений
    titles_adds: List[str] = []
    # Счетчик для среднего времени выполнения
    median_time: float = 0.0
    # Счетчик для общего времени за цикл
    count: float = 0.0
    # Получаем инициализированный браузер
    browser: webdriver.Firefox = initial_browser()

    try:
        # Цикл для ссылок авито
        for link in avito_links:
            # Отметка времени начала сбора информации из
            # первого объявления
            start_time: float = time.time()
            # получение странички по ссылке
            browser.get(link)
            try:
                # Ищем элемент в котором есть надпись о том что нет объявлений
                browser.find_element(By.CLASS_NAME, 'no-results-root-bWQVm')
                titles_adds.append('null')
                # Если такого нет вызывается исключение NoSuchElementException и мы переходим
                # в блок except
            except NoSuchElementException:
                # Получение информации о первом посте
                ad_info: Dict[str,str] = parse_first_add_avito(browser)
                # Проверка данных на валидность
                if ad_data_validator(ad_info):
                    title_ad: str = ad_info['title']
                    # date_ad: str = ad_info['date']
                    # Добавляем объявление в массив с объявлениями
                    titles_adds.append(title_ad)
                    # Находим время выполнения
                    lead_time: float = time.time() - start_time
                    # Добавляем к словарю с информацией время работы для вывода
                    ad_info['time'] = str(lead_time)
                    # Добавляем к общему счетчику времени
                    median_time += lead_time
                    # Общее время работы за один цикл
                    count += lead_time
                    # Вывод инфмормации одного объявления
                    print(beautiful_info_cmd(ad_info))
                else:
                    print(f"{'-'*60} INFO NOT FOUND OR NOT VALID{'-'*60}")

        # Находим среднее время выполнения и выводим
        print('-'*60 + '\n' + f'{" "*16}count time: {count}'.upper() + '\n' + '-'*60)
        print('-'*60 + '\n' + f'{" "*16}median time: {median_time/17}'.upper() + '\n' + '-'*60)
    except WebDriverExeption as ex:
        print(ex)
    finally:
        print('-'*60 + '\n' + f'{" "*16}End of service'.upper() + '\n' + '-'*60)
        browser.close()
        browser.quit()

if __name__ == '__main__':
    pass
