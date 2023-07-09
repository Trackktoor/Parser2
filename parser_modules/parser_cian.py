"""
    Файл с функциями для парсинга циана
"""
# Модуль для явного указания типов данных
from typing import Dict, List
from typing import Union

from datetime import datetime
from datetime import timedelta

import traceback

# Класс для посика элементов
from selenium.webdriver.common.by import By

# Исключение для обработки времени ожидания нахождения элемента на страничке
from selenium.common.exceptions import TimeoutException

# Исключение при не нахождени элемента
from selenium.common.exceptions import NoSuchElementException

# Класс webdriver нужен для инициализации бразуера
from selenium import webdriver

# Класс элемента на страничке
from selenium.webdriver.remote.webelement import WebElement

# Класс для ожиданий в Selenium
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore

# Класс для условий ожидания
from selenium.webdriver.support import expected_conditions as EC

# Таких как наведение курсора на элемент
from selenium.webdriver.common.action_chains import ActionChains

# Функция для красивого вывода информации
from helper_modules.output_data_handlers import beautiful_info_cmd


# ВЗАИМОДЕЙСТВИЕ С БРАУЗЕРОМ


def move_to_element_castom(browser: webdriver.Firefox, element: WebElement):
    """
        Функция наводится на элемент
    """
    action = ActionChains(browser)
    action.move_to_element(element).perform()


# ОБЩИЕ ФУНКЦИИ ДЛЯ СБОРА ИНФОРМАЦИИ С ОБЪЯВЛЕНИЯ


def find_element_on_page_by_class_name(browser: webdriver.Firefox, class_: str) -> Union[WebElement, None]:
    """
        Поиск элемента с помощю ожиданий по классу возвращает сам элемент если находит его
    """
    try:
        # Настройка объекта ожидания
        wait: WebDriverWait = WebDriverWait(browser, 15, poll_frequency=0.1)
        # Поиск объявления в течении 10 секунд с интервалом в 0.1 секунду
        element: WebElement = wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, class_)
        ))
        return element
    except TimeoutException:
        print(beautiful_info_cmd({'error': 'ELEMENT NOT FOUND ON 10 SECONDS'}))
        print(traceback.format_exc())
        return None


def parse_item_info_on_add_by_class_name(browser: webdriver.Firefox, class_: str) -> str:
    """
        Функция-шаблон для сбора информации по классам из 1-го объявления cian
        В случае когда элемент не найден возвращает "None"
    """
    # Поиск ифнормации
    info: Union[WebElement, None] = find_element_on_page_by_class_name(
        browser, class_)

    if info is not None:
        return info.text

    return 'None'


# ФУНКЦИИ ДЛЯ СБОРА ИНФОРМАЦИИ ПО ПОЛЯМ ОБЪЯВЛЕНИЯ

def parse_address_add_cian(parent: WebElement) -> str:
    """
        Функция для сбора адреса объявления
    """

    address = parent.find_elements(
        By.CLASS_NAME, '_93444fe79c--row--kEHOK')[1].text

    return address


def parse_price_add_cian(parent: WebElement) -> str:
    """
        Функция для сбора цены на объявление
    """
    price = parent.find_element(
        By.CLASS_NAME, '_93444fe79c--container--aWzpE').text
    # Получаем строку именно с числом без доп. символов
    price = price.replace('\xa0', '')[:-7]
    return price


def parse_url_add_cian(parent: WebElement) -> str:
    """
        Функция для сбора ссылки на объявление
    """
    ad_container = parent.find_element(
        By.CLASS_NAME, '_93444fe79c--link--eoxce').text
    return ad_container


def parse_date_add_cian(parent: WebElement) -> str:
    """
        Находит вермя первого объявления и возвращает его
        в формате datetime
        Если дата очень старая возвращает "None"
    """
    try:
        time: str = parent.find_element(
            By.CLASS_NAME, '_93444fe79c--relative--IYgur').text
        # разбиваем нашу дату так как она приходит к нам в формате
        # N минут/часов назад
        time_split: List[str] = time.split(' ')

        if 'час' in time_split[1]:
            return str(
                datetime.now() -
                timedelta(hours=int(time_split[0])) - timedelta(hours=3)
            )
        if 'мин' in time_split[1]:
            return str(
                datetime.now() -
                timedelta(minutes=int(time_split[0])) - timedelta(hours=3)
            )
    except IndexError:
        # В остальных случаях когда дата не час и не минуты назад вовзарашем 'None'
        return 'None'
    return 'None'


def parse_phone_add_cian(parent: WebElement, browser: webdriver.Firefox) -> Union[str, None]:
    """
        Функция собирает номер телефона с первого объявления на авито
    """
    try:
        # Находим контейнер кнопки
        button = find_element_on_page_by_class_name(
            browser, '_93444fe79c--button--Cp1dl')
        # _93444fe79c--button--Cp1dl
        if button is not None:
            button.click()
            # Получаем номер телефона
            phone = parent.find_elements(
                By.CLASS_NAME, '_93444fe79c--container--aWzpE')[3].text
            return phone
        return None
    except NoSuchElementException:
        return None


def parse_first_add_cian(browser: webdriver.Firefox) -> Dict[str, str]:
    """
        Собирает всю информацию о первом объявлении cian
    """

    # Родительский контейнер объявления
    parent_container = find_element_on_page_by_class_name(
        browser, '_93444fe79c--card--ibP42')
    if parent_container is not None:
        # Сбор информации с объявления

        title: str = parse_item_info_on_add_by_class_name(
            browser, '_93444fe79c--row--kEHOK')

        date: str = parse_date_add_cian(parent_container)

        phone: Union[str, None] = parse_phone_add_cian(
            parent_container, browser)

        url: str = parse_url_add_cian(parent_container)

        price: str = parse_price_add_cian(parent_container)

        address: str = parse_address_add_cian(parent_container)

        return {
            'title': title,
            'date': date,
            'phone': phone if phone is not None else 'Не найден',
            'url': url if url != 'None' else 'Не найден',
            'price': str(price) if price != 'None' else 'Не найден',
            'address': address if address != 'None' else 'Не найден',
            'marketing_source': '0'
        }
    return {'None': 'None'}


if __name__ == '__main__':
    pass
