from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Параметры для входа в систему
base_url = "https://renokom.ru/admin/"
username = "admin"
password = "my_strongest_password"

# Текст для поиска в таблице
search_text = "Все товары"

# Настройка Selenium WebDriver
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def login():
    """ Функция для входа в админ-панель OpenCart. """
    try:
        driver.get(base_url)
        driver.find_element(By.ID, "input-username").send_keys(username)
        driver.find_element(By.ID, "input-password").send_keys(password)
        driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(driver, 10).until(EC.url_contains("route=common/dashboard"))
        current_url = driver.current_url
        token_match = re.search(r'user_token=([^&]+)', current_url)
        return token_match.group(1) if token_match else None
    except Exception as e:
        print(f"Ошибка входа: {e}")
        return None

def navigate_to_page(user_token):
    """ Функция для навигации к нужной странице с использованием user_token. """
    target_url = f"https://renokom.ru/admin/index.php?route=extension/module/update_meta&user_token={user_token}"
    driver.get(target_url)

def select_checkboxes():
    """ Обычная функция для выбора чекбоксов в таблице. """
    selected_count = 0

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "table-striped")))
        rows = driver.find_elements(By.CSS_SELECTOR, ".table-striped tbody tr")

        for row in rows:
            if search_text in row.text:
                checkbox = row.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                if not checkbox.is_selected():
                    checkbox.click()
                    selected_count += 1
                    print(f"Выделено чекбоксов: {selected_count}")

        print(f"Всего выделено чекбоксов: {selected_count}")
    except Exception as e:
        print(f"Ошибка при выборе чекбоксов: {e}")

def select_checkboxes_fast():
    """ Быстрая функция для выбора чекбоксов в таблице с использованием JavaScript. """
    selected_count = 0

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "table-striped")))
        rows = driver.find_elements(By.CSS_SELECTOR, ".table-striped tbody tr")

        for row in rows:
            if search_text in row.text:
                checkbox = row.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                if not checkbox.is_selected():
                    driver.execute_script("arguments[0].click();", checkbox)
                    selected_count += 1
                    print(f"Выделено чекбоксов: {selected_count}")

        print(f"Всего выделено чекбоксов: {selected_count}")
    except Exception as e:
        print(f"Ошибка при выборе чекбоксов: {e}")

# Выполняем вход и получаем user_token
token = login()
if token:
    navigate_to_page(token)

    # True для использования быстрого метода
    use_fast_method = False

    if use_fast_method:
        select_checkboxes_fast()
    else:
        select_checkboxes()

# Ожидаем ввода от пользователя перед закрытием
input("Нажмите Enter для завершения работы...")
