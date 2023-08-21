
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


### ПОЛУЧЕНИЕ ПАРАМЕТРОВ КОНФИГУРАЦИИ ###

# создаём объекта парсера конфигурации
config = configparser.ConfigParser()
# читаем конфиг
config.read("settings.ini")

AVITO_LINKS: List[str] = [
    link.replace('\n', '') for link in config.get(
        'PARSER_LINKS',
        'avito_links'
    ).split(',')
]

CIAN_LINK: str = config.get('PARSER_LINKS', 'cian_link')

if __name__ == '__main__':
    initial_start(avito_links=AVITO_LINKS, cian_link=CIAN_LINK)
