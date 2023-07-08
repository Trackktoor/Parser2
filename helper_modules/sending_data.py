# Модуль для явного указания типов данных
from typing import Dict, List
# Модуль requests нужен для отправки запросов на сервера
import requests


def send_data_on_server(adds_info: List[Dict]):
    """
        Функция для отправки информации объявлений на сервер
    """
    for ad in adds_info:
        requests.post('http://127.0.0.1:8000/adds/request_proceed/', data={
            'date': str(ad['date']),
            'phone': ad['phone'],
            'url': ad['url'],
            'title': ad['title'],
            'price': int(ad['price']),
            'marketing_source': int(ad['marketing_source']),
            'address': ad['address']
        })
