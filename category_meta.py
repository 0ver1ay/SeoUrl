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

# Список моделей для обработки
#target_models = ["Берлинго B9", "Альмера G15", "Террано 3"]
target_models = ["Берлинго M59", "Берлинго B9", "Партнер M59", "Партнер B9", "Альмера G15"]

renault_models = ["Дастер (1 поколение)", "Аркана", "Дастер (2 поколение)", "Кангу (1 поколение)",
                  "Кангу (2 поколение)", "Каптур", "Клио (2 поколение)", "Колеос (1 поколение)",
                  "Лагуна (2 поколение)", "Логан (1 поколение)", "Логан (2 поколение)", "Флюенс",
                  "Трафик (2 поколение)", "Мастер (2 поколение)", "Мастер (3 поколение)", "Меган (2 поколение)",
                  "Меган (3 поколение)", "Сандеро (1 поколение)", "Сандеро (2 поколение)", "Симбол (1 поколение)",
                  "Симбол (2 поколение)", "Сценик (1 поколение)", "Сценик (2 поколение)", "Сценик (3 поколение)"]
peugeot_models = ["308", "Партнер M59", "Партнер B9"]
citroen_models = ["C4", "Берлинго M59", "Берлинго B9"]
lada_models = ["Ларгус"]
nissan_models = ["Альмера G15", "Террано 3"]

brands = {
    'Рено': renault_models,
    'Пежо': peugeot_models,
    'Ситроен': citroen_models,
    'Лада': lada_models,
    'Ниссан': nissan_models
}



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
def check_brand(target_model):
    for key, value in brands.items():
        if target_model in value:
            current_brand = key
            break
    return current_brand
def filter(user_token, target_models):
    for target_model in target_models:
        current_brand = check_brand(target_model)
        print(f"{current_brand} {target_model}")
        #print(f"Начало изменения SEO-URL")
        # driver.get(f"{base_url}index.php?route=catalog/category&user_token={user_token}&filter_cm=1&filter_cat={url_part}&page={page_num}")
        driver.get(f"{base_url}index.php?route=catalog/category&user_token={user_token}&filter_cm=1&filter_cm=1")
        # time.sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "ChatBtnSet")))
        filter_field = driver.find_element(By.ID, "input-cat")
        #print("Страница загружена")
        filter_field.send_keys(target_model)
        #time.sleep(0.5)

        button_filter = driver.find_element(By.ID, "button-filter")
        button_filter.click()

        change_table(target_model, current_brand)
        #time.sleep(0.5)
def change_table(target_model, current_brand):
    all_tr = driver.find_elements(By.CSS_SELECTOR, "table.table-bordered.table-hover tbody tr")
    main_window_handle = driver.current_window_handle
    # Проход по каждому элементу tr
    for tr in all_tr[1:]:
        button_element = tr.find_element(By.CSS_SELECTOR, 'a[data-toggle="tooltip"][title=""][class="btn btn-primary btn-adw-sm"]')
        #button_element.click()
        button_filter_url = button_element.get_attribute('href')
        driver.execute_script("window.open();")
        new_window_handle = driver.window_handles[-1]
        driver.switch_to.window(new_window_handle)
        driver.get(button_filter_url)
        # Дожидаемся загрузки страницы
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".chatgptseo-refresh")))
        change_category_info(target_model, current_brand)
        driver.switch_to.window(main_window_handle)
def change_category_info(target_model, current_brand):


    # Находим форму для ввода нового названия категории
    input_name = driver.find_element(By.ID, "input-name2")
    # Получаем текст из формы
    nazvanie_categorii = input_name.get_attribute('value')

    # Заполняем поля на основе названия категории
    input_h1 = driver.find_element(By.ID, "input-meta-h12")
    input_title = driver.find_element(By.ID, "input-meta-title2")
    input_description = driver.find_element(By.ID, "input-meta-description2")
    input_keywords = driver.find_element(By.ID, "input-meta-keyword2")

    # Определяем плейсхолдеры
    h1_placeholder = f"{nazvanie_categorii} для {current_brand} {target_model}"
    title_placeholder = f"Купите {nazvanie_categorii} для {current_brand} {target_model} с доставкой по Москве."
    description_placeholder = f"{nazvanie_categorii} {current_brand} {target_model} - в наличии и под заказ в Реноком. Большой ассортимент, помощь в подборе и доступные цены."
    keywords_placeholder = f" {current_brand} {target_model}, {nazvanie_categorii} {current_brand}, {nazvanie_categorii} {current_brand} {target_model}, {nazvanie_categorii} {target_model}, {nazvanie_categorii}, {current_brand}, {target_model}"

    # Записываем в поля
    input_h1.clear()
    input_h1.send_keys(h1_placeholder)
    input_title.clear()
    input_title.send_keys(title_placeholder)
    input_description.clear()
    input_description.send_keys(description_placeholder)
    input_keywords.clear()
    input_keywords.send_keys(keywords_placeholder)

    # Жмем сохранить
    save_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][form='form-category']")
    save_button.click()

    # Закрываем страницу
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ChatBtnSet")))
    driver.close()

def main():
    user_token = login()
    filter(user_token, target_models)

if __name__ == "__main__":
    try:
        main()
        input("Нажмите Enter для выхода...")  # Держим скрипт активным, пока пользователь явно не решит выйти
    except Exception as e:
        print(f"Произошла ошибка: {e}")

