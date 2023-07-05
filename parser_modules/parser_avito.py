"""
    Файл с функциями для парсинга авито
"""


# Модуль для явного указания типов данных
from typing import Dict, List

from datetime import datetime
from datetime import timedelta

import traceback

# Класс для посика элементов
from selenium.webdriver.common.by import By

# Исключение для обработки времени ожидания нахождения элемента на страничке
from selenium.common.exceptions import TimeoutException

# Класс webdriver нужен для инициализации бразуера
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait  # type: ignore

# Класс для условий ожидания
from selenium.webdriver.support import expected_conditions as EC


def parse_item_info_on_add_by_class_name(browser: webdriver.Firefox, class_: str) -> str:
    """
        Функция-шаблон для сбора информации по классам из 1-го объявления Avito
        В случае когда элемент не найден возвращает "None"
    """
    try:
        wait: WebDriverWait = WebDriverWait(browser, 10, poll_frequency=0.1)
        info: str = wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, class_)
        )).text

        return info
    except TimeoutException:
        print(traceback.format_exc())
        return "None"


def parse_date_add_avito(browser: webdriver.Firefox) -> str:
    """
        Находит вермя первого объявления и возвращает его
        в формате datetime
        Если дата очень старая возвращает "None"
    """
    time: List[str] = parse_item_info_on_add_by_class_name(
        browser,
        "iva-item-dateInfoStep-_acjp"
    ).split(' ')

    if 'час' in time[1]:
        return str(datetime.now() - timedelta(hours=int(time[0])) - timedelta(hours=3))
    elif 'мин' in time[1]:
        return str(datetime.now() - timedelta(minutes=int(time[0])) - timedelta(hours=3))
    else:
        return 'None'


def parse_first_add_avito(browser: webdriver.Firefox) -> Dict[str, str]:
    """
        Собирает всю информацию о первом объявлении Avito
    """

    title: str = parse_item_info_on_add_by_class_name(
        browser, 'styles-module-root-TWVKW')

    date: str = parse_date_add_avito(browser)

    return {
        'title': title,
        'date': date,
    }

if __name__ == '__main__':
    pass
