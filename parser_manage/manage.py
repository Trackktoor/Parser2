
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

# Класс для посика элементов
from selenium.webdriver.common.by import By




class WebDriverExeption(Exception):
    """
        Исключение для обработки ошибок WebDriver
    """
    def __str__(self) -> str:
        return str(traceback.format_exc())

def initial_browser(links):
    """
        Функция для инициализации браузера
        Возвращает экземпляр webdriver в котором
        открыты все нужные ссыллки авито
    """
    install_dir = "..\\additional_tools\\Mozilla Firefox\\"
    driver_loc = os.path.join(install_dir, "geckodriver")
    binary_loc = os.path.join(install_dir, "firefox.exe")

    service = Service(driver_loc)

    opts = webdriver.FirefoxOptions()
    opts.headless = False
    opts.set_preference('dom.webdriver.enabled', False)
    opts.binary_location = binary_loc
    opts.set_preference("log.level", "OFF")

    try:
        browser = webdriver.Firefox(service=service, options=opts)
        browser.find_element(By.CSS_SELECTOR, '[style="-webkit-line-clamp:2"]')
        for index, link in enumerate(links):
            if index == 0:
                browser.get(link)
            else:
                browser.execute_script("window.open('');")
                browser.switch_to.window(browser.window_handles[index])
                browser.get(link)
                time.sleep(1)
        browser.switch_to.window(browser.window_handles[0])
        return browser
    except WebDriverExeption as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()

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

if __name__ == '__main__':
    initial_browser(AVITO_LINKS)
    time.sleep(2)
