
"""
    Это менеджер парсера в котором используется весь функционал модулей
    для получения и отправки данных.
"""

# Модуль для явного указания типов данных в этом импорте List
from typing import List

# библиотека для обработки конфигурационных даннхы из ini файлов
import configparser


# Функция для инициализации старта всего сервиса
from helper_modules.webdriver_handlers import initial_start


# создаём объекта парсера
config = configparser.ConfigParser()
# читаем конфиг
config.read("settings.ini")

AVITO_LINKS: List[str] = [
    link.replace('\n', '') for link in config.get(
        'PARSER_LINKS',
        'avito_links'
    ).split(',')
]
# pylint: disable=line-too-long
CIAN_LINK: str = 'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&sort=creation_date_desc&type=4'
# pylint: enable=line-too-long


if __name__ == '__main__':
    initial_start(avito_links=AVITO_LINKS,
                  cian_link=CIAN_LINK)
