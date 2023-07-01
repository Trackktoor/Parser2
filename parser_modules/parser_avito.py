from ..parser_manage import manage as manage
from selenium.webdriver.common.by import By


def run_parse_avito(browser):
    browser.find_element(By.CSS_SELECTOR, '[style="-webkit-line-clamp:2"]')
