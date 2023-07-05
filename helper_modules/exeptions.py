"""
    Файл с кастомными Exeption
"""

# Модуль для трасировок из интерпритатора Python
import traceback

class WebDriverExeption(Exception):
    """
        Исключение для обработки ошибок WebDriver
    """
    def __str__(self) -> str:
        return str(traceback.format_exc())

if __name__ == '__main__':
    pass
