"""
    Файл с функциями для преобразования данных в понятный текст
"""

# Модуль для явного указания типов данных
from typing import Dict


def beautiful_info_cmd(log: Dict[str, str]) -> str:
    """
        Функция для красивого вывода информации в консоль
        Принимает словарь с str,str и вывод ключ:значение в красивом формате
    """
    def format_str(max_len) -> str:
        res_log: str = f'\n{"-"*max_len}\n'
        for title, value in log.items():
            res_log += f"{title}:{value}\n"
        res_log += '-'*max_len
        return res_log

    max_len: int = max([el_len for el_len in map(len, log.values())])
    return format_str(60) if max_len < 60 else format_str(max_len)


if __name__ == '__main__':
    pass
