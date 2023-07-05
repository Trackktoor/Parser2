"""
    Файл с функциями для провреки данных на валидность
"""

# Модуль для явного указания типов данных
from typing import Dict


def ad_data_validator(data: Dict[str, str]) -> bool:
    """
        Функция для проверки данных на валидность

        data: Словарь данных в котором элементы проверяются на наличие данных 
    """
    for value in data.values():
        if value == 'None':
            return False
    return True


if __name__ == '__main__':
    pass
