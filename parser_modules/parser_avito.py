"""
    Файл с функциями для парсинга авито
"""


# Класс для посика элементов
from selenium.webdriver.common.by import By

# Класс для ожиданий в Selenium
from selenium.webdriver.support.ui import WebDriverWait

# Класс для условий ожидания
from selenium.webdriver.support import expected_conditions as EC


def parse_first_add_avito(browser):
    """
        Собирает всю информацию о первом объявлении Avito
    """
    print('wait...')
    wait = WebDriverWait(browser, 10, poll_frequency=0.1)
    title = wait.until(EC.visibility_of_element_located(
        (By.CLASS_NAME, 'styles-module-root-TWVKW')
    )).text

    return title
