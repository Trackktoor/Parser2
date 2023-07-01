
"""
    Это менеджер парсера в котором используется весь функционал модулей
    для получения и отправки данных.
"""

# Модуль os в Python предоставляет функции для взаимодействия с операционной системой.
import os

# Модуль os в Python предоставляет функции для взаимодействия с операционной системой.
import time

# Модуль для трасировок из интерпритатора Python
import traceback

# Модули Selenium

# Класс webdriver нужен для инициализации бразуера
from selenium import webdriver

# Service нужен для конфигурации и запуска экземпляра webdriver(браузер)
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException

from parser_modules.parser_avito import parse_first_add_avito

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class WebDriverExeption(Exception):
    """
        Исключение для обработки ошибок WebDriver
    """
    def __str__(self) -> str:
        return str(traceback.format_exc())

def scroll_down(passed_in_driver):
    """
        Функция для скролла странички вниз на 200px
    """

    scroll_nav_out_of_way = 'window.scrollBy(0, 200);'
    passed_in_driver.execute_script(scroll_nav_out_of_way)

def initial_browser():
    """
        Функция для инициализации браузера
        Возвращает экземпляр webdriver в котором
        открыты все нужные ссыллки авито
    """
    install_dir = ".\\additional_tools\\Mozilla Firefox\\"
    driver_loc = os.path.join(install_dir, "geckodriver")
    binary_loc = os.path.join(install_dir, "firefox.exe")

    service = Service(driver_loc)

    opts = webdriver.FirefoxOptions()
    opts.set_preference('dom.webdriver.enabled', False)
    opts.add_argument('-headless')
    opts.binary_location = binary_loc
    opts.set_preference("log.level", "OFF")
    opts.page_load_strategy = 'none'

    browser = webdriver.Firefox(service=service, options=opts)

    return browser

# pylint: disable=line-too-long
AVITO_LINKS = [
    'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?f=ASgBAgICA0SSA8gQ8AeQUsDBDbr9Nw&localPriority=0&p=1&s=104&user=1',
    'https://www.avito.ru/reutov/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/lyubertsy/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/mytischi/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/balashiha/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/scherbinka/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?user=1&s=104',
    'https://www.avito.ru/moskovskaya_oblast_krasnogorsk/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/kommunarka/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/zarechye/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/odintsovo/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/himki/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/moskovskaya_oblast/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?q=%D1%82%D0%BE%D0%BC%D0%B8%D0%BB%D0%B8%D0%BD%D0%BE&s=104&user=1',
    'https://www.avito.ru/irkutskaya_oblast_zheleznodorozhnyy/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/kotelniki/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/dzerzhinskiy/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?q=%D0%B4%D0%B7%D0%B5%D1%80%D0%B6%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9&s=104&user=1',
    'https://www.avito.ru/irkutskaya_oblast_zheleznodorozhnyy/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?q=%D0%B4%D0%BE%D0%BB%D0%B3%D0%BE%D0%BF%D1%80%D1%83%D0%B4%D0%BD%D1%8B%D0%B9&s=104&user=1',
    'https://www.avito.ru/podolsk/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1',
    'https://www.avito.ru/tyumenskaya_oblast_moskovskiy/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1'
]
CIAN_LINK = 'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&sort=creation_date_desc&type=4'
# pylint: enable=line-too-long

TIME_SLEEP = 1

def initial_start(avito_links, cian_link):
    """
        Функция для старта всего сервиса
        Собирает все модули в одном месте и управляет ими
    """
    titles_adds = []
    median_time = 0

    browser = initial_browser()

    try:
        for link in avito_links:
            start_time = time.time()
            browser.get(link)
            try:
                browser.find_element(By.CLASS_NAME, 'no-results-root-bWQVm')
                titles_adds.append('null')
            except NoSuchElementException:
                title_ad = parse_first_add_avito(browser)
                titles_adds.append(title_ad)
                time.sleep(TIME_SLEEP)

                median_time += time.time() - start_time
                print(f"--- {time.time() - start_time} seconds ---" % ())
        print('-'*60 + '\n' + f'{" "*16}median time: {median_time/17}'.upper() + '\n' + '-'*60)
    except WebDriverExeption as ex:
        print(ex)
    finally:
        print('-'*60 + '\n' + f'{" "*16}End of service'.upper() + '\n' + '-'*60)
        browser.close()
        browser.quit()

if __name__ == '__main__':
    initial_start(AVITO_LINKS,CIAN_LINK)
    time.sleep(2)
