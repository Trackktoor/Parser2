"""
    Файл с функциями для обработки и взаимодействия с браузеорм
"""

# Модуль os в Python предоставляет функции для взаимодействия с операционной системой.
import os

import time

# Модуль для асинхронных операций
import asyncio

# Модуль для явного указания типов данных
from typing import List, Dict


# Модули Selenium
# Класс webdriver нужен для инициализации бразуера
from selenium import webdriver

# Класс для поиска элементов на страничке (по классам, id и т.д.)
from selenium.webdriver.common.by import By
# Исключение Selenium которое вызывается при не нахождении элемента
from selenium.common.exceptions import NoSuchElementException
# Service нужен для конфигурации и запуска экземпляра webdriver(браузер)
from selenium.webdriver.firefox.service import Service
# Класс ActionChains используется для выполнения действий на страничке


# Вспомогательные функции
# Функция для сбора информации о первом элементе с странички Avito
from parser_modules.parser_avito import parse_first_add_avito
# Функция для сбора информации о первом элементе с странички Cian
from parser_modules.parser_cian import parse_first_add_cian

# Исключение для обработки ошибок WebDriver
from helper_modules.exeptions import WebDriverExeption
# Валидатор данных объявления
from helper_modules.validators import ad_data_validator
# Функция для красивого вывода данных
from helper_modules.output_data_handlers import beautiful_info_cmd

from helper_modules.sending_data import send_data_on_server


def scroll_down(passed_in_driver: webdriver.Firefox):
    """
        Функция для скролла странички вниз на 200px
    """
    scroll_nav_out_of_way: str = 'window.scrollBy(0, 300);'
    passed_in_driver.execute_script(scroll_nav_out_of_way)


def initial_browser() -> webdriver.Firefox:
    """
        Функция для инициализации браузера
        Возвращает экземпляр webdriver
    """
    install_dir: str = ".\\additional_tools\\Mozilla Firefox\\"
    # Путь до драйвер браузера
    driver_loc: str = os.path.join(install_dir, "geckodriver")
    # Сам браузере .exe
    binary_loc: str = os.path.join(install_dir, "firefox.exe")

    service: Service = Service(driver_loc)

    opts: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
    opts.set_preference('useAutomationExtension', False)
    opts.set_preference("dom.webdriver.enabled", False)
    opts.set_preference('devtools.jsonview.enabled', False)
    opts.add_argument("--width=240")
    opts.add_argument("--height=50")
    opts.set_preference("general.useragent.override",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 RuxitSynthetic/1.0 v3117066926825241668 t154204124582458670 ath1fb31b7a altpriv cvcv=2 cexpw=1 smf=0")
    # Параметр для отключения графческой оболочки
    # opts.add_argument('-headless')
    opts.binary_location = binary_loc
    # Отключение логов
    opts.set_preference("log.level", "OFF")
    # Стратегия загрузки страницы
    opts.page_load_strategy = 'eager'

    browser: webdriver.Firefox = webdriver.Firefox(
        service=service, options=opts)

    return browser

# pylint: disable=line-too-long


# type: ignore
def initial_start(avito_links: List[str], cian_link: str):
    """
        Функция для старта всего сервиса
        Собирает все модули в одном месте и управляет ими
    """
# pylint: enable=line-too-long
    # Массив для объявлений
    adds_info: List[Dict] = []
    # Счетчик для среднего времени выполнения
    median_time: float = 0.0
    # Счетчик для общего времени за цикл
    count: float = 0.0
    # Получаем инициализированный браузер
    browser: webdriver.Firefox = initial_browser()

    try:
        # Сбор данных с циана
        browser.set_window_size(100, 100)
        browser.get(cian_link)
        browser.set_window_size(1200, 760)
        ad_info: Dict[str, str] = parse_first_add_cian(browser)
        # Отправка данных на сервер
        asyncio.run(send_data_on_server([ad_info]))
        # Вывод информации
        print(beautiful_info_cmd(ad_info))
        # Цикл для ссылок авито
        for link in avito_links:
            # Отметка времени начала сбора информации из
            # первого объявления
            start_time: float = time.time()
            # получение странички по ссылке
            browser.set_window_size(200, 250)
            time.sleep(2.5)
            browser.get(link)
            browser.set_window_size(1150, 660)

            # Производиться скролл для того чтобы объявление было в зоне видимости
            scroll_down(browser)

            try:
                # Ищем элемент в котором есть надпись о том что нет объявлений
                browser.find_element(By.CLASS_NAME, 'no-results-root-bWQVm')
                adds_info.append({'null': 'null'})
                # Если такого нет вызывается исключение NoSuchElementException и мы переходим
                # в блок except
            except NoSuchElementException:
                # Получение информации о первом посте
                ad_info: Dict[str, str] = parse_first_add_avito(browser)
                time.sleep(3)
                # Проверка данных на валидность
                if ad_data_validator(ad_info):
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
                    # Отправляем собранные
                    asyncio.run(send_data_on_server([ad_info]))
                else:
                    print(beautiful_info_cmd(
                        {'error_info': 'INFO NOT FOUND OR NOT VALID'}))

        # Выводим общее рвемя выполнения за один цикл
        print('-'*60 + '\n' +
              f'{" "*16}count time: {count}'.upper() + '\n' + '-'*60)
        # Находим среднее время выполнения и выводим
        print('-'*60 + '\n' +
              f'{" "*16}median time: {median_time/17}'.upper() + '\n' + '-'*60)
    except WebDriverExeption as ex:
        print(ex)
    finally:
        print(beautiful_info_cmd({'end': 'End of service'}))
        browser.close()
        browser.quit()


if __name__ == '__main__':
    pass
