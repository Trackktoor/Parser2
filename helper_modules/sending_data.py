"""
    Файл с функциями для отправки данных на сервер
"""

# Модуль для явного указания типов данных
from typing import Dict, List
# Модуль requests нужен для отправки запросов на сервера
import requests


def send_data_on_server(adds_info: List[Dict]):
    """
        Функция для отправки информации объявлений на сервер
    """
    for item in adds_info:
        requests.post('http://elka18pl.beget.tech/request_proceed/', data={
            'date': str(item['date']),
            'phone': item['phone'],
            'url_data': item['url'],
            'title': item['title'],
            'price': int(item['price'].replace(' ', '')),
            'marketing_source': int(item['marketing_source']),
            'address': item['address']
        }, timeout=1)
