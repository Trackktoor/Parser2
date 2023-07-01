from selenium.webdriver.common.by import By


# Функция с запросом
def click_button_number(browser):
    pass


def get_info(browser):
    """
        Функция для сбора всей информации с объявления
        используя вспомогательные функции
    """
    first_ad = get_first_ad(browser)

    date = get_date_ad(first_ad)
    url_data = get_url_ad(first_ad)
    title = get_title_ad(first_ad)
    price = get_price_ad(first_ad)
    marketing_source = 2
    phone = get_phone_number_ad(browser)
    address = get_address_ad(first_ad)

    result = {
        'date': date,
        'url_data': url_data,
        'title': title,
        'price': price,
        'marketing_source': marketing_source,
        'phone': phone,
        'address': address,
    }

    return result
