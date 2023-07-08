"""
    Файл с функциями для парсинга авито
"""


# Модуль для явного указания типов данных
from typing import Dict, List
from typing import Union

from datetime import datetime
from datetime import timedelta

import traceback

# Библиотека для работы с ОС
import os

# Функция для декодировния из Base64
from base64 import b64decode

# Библиотека для обработки изображений
import cv2

# Библиотека для чтения текста с изображения
import pytesseract

# Класс для посика элементов
from selenium.webdriver.common.by import By

# Исключение для обработки времени ожидания нахождения элемента на страничке
from selenium.common.exceptions import TimeoutException

# Класс webdriver нужен для инициализации бразуера
from selenium import webdriver

# Класс элемента на страничке
from selenium.webdriver.remote.webelement import WebElement

# Класс для ожиданий в Selenium
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore

# Класс для условий ожидания
from selenium.webdriver.support import expected_conditions as EC

# Класс элемента на страничке
from selenium.webdriver.remote.webelement import WebElement

# Таких как наведение курсора на элемент
from selenium.webdriver.common.action_chains import ActionChains

# Функция для красивого вывода информации
from helper_modules.output_data_handlers import beautiful_info_cmd

# Функция для наведения курсора на элемент


def move_to_element_castom(browser: webdriver.Firefox, element: WebElement):
    """
        Функция наводится на элемент
    """
    action = ActionChains(browser)
    action.move_to_element(element).perform()


def find_element_on_page_by_class_name(browser: webdriver.Firefox, class_: str) -> Union[WebElement, None]:
    """
        Поиск элемента с помощю ожиданий по классу возвращает сам элемент если находит его
    """
    try:
        wait: WebDriverWait = WebDriverWait(browser, 10, poll_frequency=0.1)
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
        Функция-шаблон для сбора информации по классам из 1-го объявления Avito
        В случае когда элемент не найден возвращает "None"
    """
    info: Union[WebElement, None] = find_element_on_page_by_class_name(
        browser, class_)
    if info is not None:
        return info.text

    return 'None'


def parse_date_add_avito(browser: webdriver.Firefox) -> str:
    """
        Находит вермя первого объявления и возвращает его
        в формате datetime
        Если дата очень старая возвращает "None"
    """
    time: str = parse_item_info_on_add_by_class_name(
        browser,
        "iva-item-dateInfoStep-_acjp"
    )
    if time != 'None':
        time_split: List[str] = time.split(' ')

        if 'час' in time_split[1]:
            return str(datetime.now() - timedelta(hours=int(time_split[0])) - timedelta(hours=3))
        if 'мин' in time_split[1]:
            return str(datetime.now() - timedelta(minutes=int(time_split[0])) - timedelta(hours=3))
    return 'None'


def parse_phone_add_avito(browser: webdriver.Firefox) -> Union[str, None]:
    """
        Функция собирает номер телефона с первого объявления на авито
    """
    def save_image_on_src(src) -> str:
        """
            Функция для сохранения фото номера телефона как phone_image.png
            Возвращает название файла: phone_image.png
        """
        encoded = src.split("base64,", 1)[1]
        data = b64decode(encoded)

        out = open("phone_image.png", 'wb')
        out.write(data)
        out.close()
        return 'phone_image.png'

    def read_img(img_name: str) -> str:
        """
            Функция переводи картинку в .jpg читает с нё текст
            и удаляет саму картинку возвращая при этом текст,
            который на ней находился
        """
        pytesseract.pytesseract.tesseract_cmd = '.\\additional_tools\\tesseract\\tesseract.exe'

        image = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)

        trans_mask = image[:, :, 3] == 0

        image[trans_mask] = [255, 255, 255, 255]

        new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        cv2.imwrite('phone_image.jpg', new_img)

        img_str = pytesseract.image_to_string('phone_image.jpg')

        os.remove(img_name)

        return img_str

    def get_phone_number_on_image(src: str):
        phone_image = save_image_on_src(src)
        phone_str = read_img(phone_image)

        return phone_str

    # Находим контейнер кнопки
    button_container = find_element_on_page_by_class_name(
        browser, 'iva-item-aside-GOesg')
    if button_container is not None:
        # Если находим контейнер с кнопкой то наводимся на него
        move_to_element_castom(browser, button_container)
        # Получаем кнопку
        button = find_element_on_page_by_class_name(browser, 'desktop-1hb0oo7')
        if button is not None:
            button.click()
            # Ищем изображение номер телефона
            phone_image = find_element_on_page_by_class_name(
                browser, 'button-phone-image-LkzoU')

            if phone_image is not None:
                # Получаем src изображения
                src_image = phone_image.get_attribute('src')
                print('src_image: OK')
                if src_image is not None:
                    phone_number = get_phone_number_on_image(src_image)
                    return phone_number
    return None


def parse_first_add_avito(browser: webdriver.Firefox) -> Dict[str, str]:
    """
        Собирает всю информацию о первом объявлении Avito
    """

    title: str = parse_item_info_on_add_by_class_name(
        browser, 'styles-module-root-TWVKW')

    date: str = parse_date_add_avito(browser)

    phone: Union[str, None] = parse_phone_add_avito(browser)

    return {
        'title': title,
        'date': date,
        'phone': phone if phone is not None else 'Не найден',
    }


if __name__ == '__main__':
    pass
