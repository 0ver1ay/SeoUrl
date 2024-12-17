from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException  # Импортируем NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

# Параметры для входа в систему
base_url = "https://renokom.ru/admin/"
username = "bender"
password = "L$@56###4h2%2^^^1xs!*uU"
seo_suffix = "-duster-1"

# Настройка Selenium WebDriver
options = webdriver.ChromeOptions()
options.headless = False  # Установите True, если не нужно открывать браузер
driver = webdriver.Chrome(options=options)

def login():
    """ Функция для входа в админ-панель OpenCart. """
    driver.get(base_url)
    driver.find_element(By.ID, "input-username").send_keys(username)
    driver.find_element(By.ID, "input-password").send_keys(password)
    driver.find_element(By.TAG_NAME, "button").click()

    # Ожидаем редиректа на главную страницу админ-панели и извлекаем user_token
    WebDriverWait(driver, 10).until(EC.url_contains("route=common/dashboard"))
    current_url = driver.current_url
    token_match = re.search(r'user_token=([^&]+)', current_url)
    return token_match.group(1) if token_match else None


def change_seo_url(user_token, page_num):
    try:
        print(f"Изменение SEO-URL на странице {page_num}...")
        driver.get(
            f"{base_url}index.php?route=catalog/category&user_token={user_token}&filter_cm=1&filter_cat=%D0%94%D0%B0%D1%81%D1%82%D0%B5%D1%80+%281&page={page_num}")

        # Явное ожидание загрузки страницы
        time.sleep(5)  # Ожидание 5 секунд для полной загрузки страницы

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "hide_seourl")))

        seourl_cells = driver.find_elements(By.CLASS_NAME, "hide_seourl")

        if page_num == 1:
            seourl_cells.pop(0)  # Пропускаем первое поле на первой странице

        for cell in seourl_cells:
            key_div = WebDriverWait(cell, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "key")))
            key_link = WebDriverWait(key_div, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "a")))

            driver.execute_script("arguments[0].scrollIntoView(true);", key_link)
            driver.execute_script("arguments[0].click();", key_link)

            input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ssort")))
            current_value = input_field.get_attribute("value")

            suffix_to_add = seo_suffix
            added_number = 0

            while True:
                if current_value.endswith(suffix_to_add):
                    break

                input_field.clear()
                input_field.send_keys(current_value + suffix_to_add)

                save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button-schange")))
                save_button.click()
                time.sleep(3)

                error_messages = driver.find_elements(By.ID, "serror")
                if error_messages:
                    print(f"Ошибка: {error_messages[0].text}")
                    added_number += 1
                    suffix_to_add = f"-{added_number}-{seo_suffix}"
                else:
                    break

    except Exception as e:
        print(f"Ошибка при изменении SEO-URL на странице {page_num}: {e}")


def logout():
    """ Функция для выхода из системы. """
    # Переходим на страницу выхода
    driver.get(f"{base_url}index.php?route=common/logout&user_token={user_token}")

# Основной скрипт
try:
    user_token = login()
    if user_token:
        current_page = 1
        last_page_reached = False

        while not last_page_reached:
            change_seo_url(user_token, current_page)

            # Пытаемся найти и нажать на кнопку "Следующая страница"
            next_page_buttons = driver.find_elements(By.CLASS_NAME, "pagination__next")
            if next_page_buttons:
                next_page_buttons[0].click()
                current_page += 1
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "key")))  # Ожидаем загрузку следующей страницы
            else:
                last_page_reached = True

    else:
        print("Не удалось получить user_token")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    logout()
    driver.quit()
