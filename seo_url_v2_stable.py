from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from transliterate import translit
import time
import re
from pymystem3 import Mystem

# Параметры для входа в систему
base_url = "https://renokom.ru/admin/"
username = "admin"
password = "my_strongest_password"

# Пары SEO Suffix и URL Part
seo_url_suffixes = ["Берлинго B9"]

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

        # Ожидаем редиректа на главную страницу админ-панели и извлекаем user_token
        WebDriverWait(driver, 10).until(EC.url_contains("route=common/dashboard"))
        current_url = driver.current_url
        token_match = re.search(r'user_token=([^&]+)', current_url)
        return token_match.group(1) if token_match else None
    except Exception as e:
        print(f"Ошибка входа: {e}")
        return None
def filter(user_token, seo_url_suffixes):
    for seo_url_suffix in seo_url_suffixes:
        print(f"Начало изменения SEO-URL")
        # driver.get(f"{base_url}index.php?route=catalog/category&user_token={user_token}&filter_cm=1&filter_cat={url_part}&page={page_num}")
        driver.get(f"{base_url}index.php?route=catalog/category&user_token={user_token}&filter_cm=1&filter_cm=1")
        # time.sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "ChatBtnSet")))
        filter_field = driver.find_element(By.ID, "input-cat")
        print("Страница загружена")
        button_filter = driver.find_element(By.ID, "button-filter")
        filter_field.send_keys(seo_url_suffix)
        time.sleep(0.5)
        button_filter.click()

        change_table(seo_url_suffix)

        time.sleep(2)
def change_table(seo_url_suffix):
    all_tr = driver.find_elements(By.CSS_SELECTOR, "table.table-bordered.table-hover tbody tr")
    # Проход по каждому элементу tr
    for tr in all_tr[1:]:
        hide_name_element = tr.find_element(By.CSS_SELECTOR, "td.text-left.hide_name")
        link_element = hide_name_element.find_element(By.CSS_SELECTOR, "a[href]")
        link_text = link_element.text

        transliterated_text = custom_transliterate(link_text)
        #print(transliterated_text)

        a_element = tr.find_element(By.CSS_SELECTOR, "div.key a[data-toggle='name']")
        a_element.click()
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "ssort")))
        # Дождаться появления и найти элемент <input id="ssort"> внутри открывшегося элемента
        input_element = tr.find_element(By.ID, "ssort")
        input_element.clear()

        input_element.send_keys(transliterated_text + "-" + custom_transliterate(seo_url_suffix))

        # Найти и нажать на кнопку <button id="button-schange">
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "button-schange")))
        button_element = tr.find_element(By.ID, "button-schange")
        button_element.click()
        time.sleep(1)
def custom_transliterate(link_text):
    # Словарь транслитерации
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    # Проходим по каждому символу в строке, транслитерируя его
    transliterated = ''.join(translit_dict.get(char, char) for char in link_text.lower())

    # Преобразуем результат в формат, пригодный для SEO URL
    seo_ready = re.sub(r'[^a-z0-9\s]', '', transliterated)  # Удаление недопустимых символов
    seo_ready = seo_ready.replace(' ', '-').replace('--', '-')  # Замена пробелов и двойных тире
    return seo_ready.rstrip('-')  # Удаление тире в конце строки

def main():
    user_token = login()
    filter(user_token, seo_url_suffixes)

if __name__ == "__main__":
    try:
        main()
        input("Нажмите Enter для выхода...")  # Держим скрипт активным, пока пользователь явно не решит выйти
    except Exception as e:
        print(f"Произошла ошибка: {e}")

