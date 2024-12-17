from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import re

# Параметры для входа в систему
base_url = "https://renokom.ru/admin/"
username = "bender"
password = "L$@56###4h2%2^^^1xs!*uU"

# Пары SEO Suffix и URL Part
seo_url_pairs = [("-partner-1-m59", "Партнер+%281+поколение%29+M59"), ("-partner-2-b9", "Партнер+%282+поколение%29+B9"),
                 ("-spacetourer", "Спейс+турер"), ("-jumpy-4", "Джампи+%284"), ("-jumper-3", "Джампер+%283"),
                 ("-berlingo-1-m59", "Берлинго+%281"), ("-berlingo-2-b9", "Берлинго+%282"), ("-c-crosser", "С-Кроссер"),
                 ("-c-elysee", "С-Элизе"), ("-c1", "С1"), ("-c3-1", "С3+%281"),
                 ("-c3-2", "С3+%282"), ("-c3-picasso", "С3+Пикассо"), ("-c4-1", "С4+%281"),
                 ("-c4-2", "С4+%282"), ("-c4-picasso-1", "С4+Пикассо+%281"), ("-c4-picasso-2", "С4+Пикассо+%282"),
                 ("-c5", "С5"), ("-largus", "Ларгус"), ("-almera", "Альмера"),
                 ("-primastar", "Примастар"), ("-terrano-3", "Террано")]

# Настройка Selenium WebDriver
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(options=options)

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

def change_seo_url(user_token, page_num, seo_suffix, url_part):
    try:
        print(f"Начало изменения SEO-URL на странице {page_num} для {url_part}")
        driver.get(f"{base_url}index.php?route=catalog/category&user_token={user_token}&filter_cm=1&filter_cat={url_part}&page={page_num}")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "hide_seourl")))
        print("Страница загружена")

        seourl_cells = driver.find_elements(By.CLASS_NAME, "hide_seourl")
        print(f"Найдено {len(seourl_cells)} элементов для изменения")

        if page_num == 1:
            seourl_cells.pop(0)  # Пропускаем первое поле на первой странице
            print("Пропущено первое поле на первой странице")

        for cell in seourl_cells:
            try:
                key_div = cell.find_element(By.CLASS_NAME, "key")
                key_link = key_div.find_element(By.TAG_NAME, "a")

                driver.execute_script("arguments[0].scrollIntoView(true);", key_link)
                driver.execute_script("arguments[0].click();", key_link)

                input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ssort")))
                current_value = input_field.get_attribute("value")

                suffix_to_add = seo_suffix
                added_number = 0

                while True:
                    if current_value.endswith(suffix_to_add):
                        print(f"Поле уже содержит суффикс: {current_value}")
                        break

                    input_field.clear()
                    input_field.send_keys(current_value + suffix_to_add)

                    save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button-schange")))
                    save_button.click()
                    time.sleep(2)

                    error_messages = driver.find_elements(By.ID, "serror")
                    if error_messages:
                        print(f"Ошибка: {error_messages[0].text}")
                        added_number += 1
                        suffix_to_add = f"-{added_number}{seo_suffix}"
                    else:
                        print(f"SEO URL изменен на: {current_value + suffix_to_add}")
                        break
            except Exception as e:
                print(f"Ошибка при изменении SEO-URL в ячейке: {e}")

    except Exception as e:
        print(f"Ошибка при изменении SEO-URL на странице {page_num} для {url_part}: {e}")

def logout():
    try:
        print("Попытка выхода из системы...")
        driver.get(f"{base_url}index.php?route=common/logout")
        print("Выход выполнен")
    except Exception as e:
        print(f"Ошибка при выходе из системы: {e}")

try:
    user_token = login()
    if user_token:
        for seo_suffix, url_part in seo_url_pairs:
            print(f"Начало работы с парой: SEO Suffix: {seo_suffix}, URL Part: {url_part}")
            current_page = 1
            last_page_reached = False

            while not last_page_reached:
                change_seo_url(user_token, current_page, seo_suffix, url_part)

                next_page_buttons = driver.find_elements(By.CLASS_NAME, "pagination__next")
                if next_page_buttons and len(next_page_buttons) > 0:
                    next_page_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(next_page_buttons[0]))
                    next_page_button.click()
                    current_page += 1
                    print(f"Переход на страницу {current_page}")
                    time.sleep(5)
                else:
                    last_page_reached = True
                    print("Последняя страница достигнута для текущей пары")
            print(f"Завершение работы с парой: SEO Suffix: {seo_suffix}, URL Part: {url_part}")
    else:
        print("Не удалось получить user_token")
except Exception as e:
    print(f"Общая ошибка скрипта: {e}")
finally:
    logout()
    driver.quit()
    print("Драйвер закрыт")
