from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import re

# Параметры для входа в систему
base_url = "https://renokom.ru/admin/"
username = "bender"
password = "L$@56###4h2%2^^^1xs!*uU"

# Искать конкретный товар
product_name = "Амортизатор передний"

# Настройка Selenium WebDriver
options = webdriver.ChromeOptions()
options.headless = False  # Убедитесь, что headless режим отключен, если хотите видеть UI
driver = webdriver.Chrome(options=options)
driver.maximize_window()  # Добавляем эту строку для открытия браузера на полный экран


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
def search_product_by_name(token, product_name):
    """Функция для поиска товара по названию в админ-панели OpenCart."""
    try:
        # Строим URL для перехода на страницу каталога товаров с использованием токена пользователя
        products_url = f"https://renokom.ru/admin/index.php?route=catalog/product&user_token={token}"
        driver.get(products_url)

        # Ожидаем, пока страница полностью загрузится
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input-name")))

        # Находим поле для ввода названия товара и вводим название
        driver.find_element(By.ID, "input-name").send_keys(product_name)

        # Находим кнопку для применения фильтра и кликаем по ней
        filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button-filter")))
        filter_button.click()

        # Ожидаем результатов фильтрации
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-responsive")))

        print("Поиск выполнен. Начинаем обработку каждого товара.")

        # Открываем каждый товар в новой вкладке и выполняем действия
        open_each_product_in_new_tab()
        driver.close()
    except Exception as e:
        print(f"Ошибка при поиске товара: {e}")
def open_each_product_in_new_tab():
    """Функция для открытия каждого товара в новой вкладке и выполнения действий на них."""

    product_links = driver.find_elements(By.CSS_SELECTOR, "a.btn-primary[data-toggle='tooltip'][data-original-title='Редактировать']")
    print("Элементы найдены")
    main_window_handle = driver.current_window_handle
    for link in product_links:
        print(link.get_attribute('href'))
        product_url = link.get_attribute('href')
        # Убедитесь, что URL содержит нужный user_token
        #print(f"Открываем URL товара: {product_url}")  # Для отладки

        driver.execute_script("window.open();")  # Открывает новую вкладку
        new_window_handle = driver.window_handles[-1]
        driver.switch_to.window(new_window_handle)  # Переключается на новую вкладку
        driver.get(product_url)  # Переходит на страницу товара
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".chatgptseo-refresh")))
        # Выполнение действий на странице товара
        # Эта функция должна быть определена в другом месте вашего скрипта
        perform_actions_and_save_product()
        driver.switch_to.window(main_window_handle)
def perform_actions_and_save_product():
    """Функция для выполнения действий на странице товара, сохранения изменений и ожидания подтверждения."""
    "Меняем параметры товара"
    change_product()

    # Находим кнопку сохранения и кликаем по кнопке "Сохранить"
    save_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][form='form-product']")
    save_button.click()

    # Ожидаем, пока не появится элемент, сигнализирующий о том, что изменения сохранены
    (print("Ожидаем, пока не появится элемент, сигнализирующий о том, что изменения сохранены"))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "button-filter")))
    (print("Элемент появился, изменения сохранены, можно закрывать вкладку"))
    # Элемент появился, изменения сохранены, можно закрывать вкладку
    driver.close()
def change_product():
    """Функция для изменения характеристик товара. h1, title, description на основе названия, артикула и производителя товара"""
    # print("Мы дошли до изменения продукта, ожидаем")
    # Находим форму для ввода нового названия товара
    input_name2 = driver.find_element(By.ID, "input-name2")
    # Получаем текст из формы
    nazvanie_tovara = input_name2.get_attribute('value')
    # Пример использования нового текста
    print("Обработка товара:", nazvanie_tovara)
    # Переходим ко вкладке "Характеристики"
    characteristics_link = driver.find_element(By.CSS_SELECTOR, "a[href='#tab-attribute']")
    characteristics_link.click()
    # Ищем поле "Бренд"
    #textarea = driver.find_element(By.NAME, "product_attribute[0]")
    textarea = driver.find_element(By.CSS_SELECTOR, "textarea[name*='product_attribute[0]']")
    # Получаем содержимое текстового поля
    brand = textarea.get_attribute('value')
    # Переходим ко вкладке "Данные"
    dannye_link = driver.find_element(By.CSS_SELECTOR, "a[href='#tab-data']")
    dannye_link.click()
    textarea = driver.find_element(By.NAME, "sku")
    # Получаем содержимое текстового поля
    sku = textarea.get_attribute('value')
    print(nazvanie_tovara + " " + brand + " " + sku)

    # Используем полученные данные
    # Переходим ко вкладке "Общие"
    general_link = driver.find_element(By.CSS_SELECTOR, "a[href='#tab-general']")
    general_link.click()

    h1_element = driver.find_element(By.ID, "input-meta-h12")
    h1_value = f"{nazvanie_tovara} {brand} {sku}"
    h1_element.clear()  # Очищаем поле перед вводом нового значения
    h1_element.send_keys(h1_value) # Вставляем данные

    title_element = driver.find_element(By.ID, "input-meta-title2")
    title_value = f"Купите {nazvanie_tovara} {brand} {sku} в Москве"
    title_element.clear()  # Очищаем поле перед вводом нового значения
    title_element.send_keys(title_value)  # Вставляем данные

    description_element = driver.find_element(By.ID, "input-meta-description2")
    description_value = f"{brand} {sku} {nazvanie_tovara} в наличии. Большой выбор, помощь в подборе, низкие цены, быстрая доставка по Москве."
    description_element.clear()  # Очищаем поле перед вводом нового значения
    description_element.send_keys(description_value)  # Вставляем данные

    keywords_element = driver.find_element(By.ID, "input-meta-keyword2")
    keywords_value = f"{nazvanie_tovara}, {brand} {sku}, {nazvanie_tovara} {brand} {sku}, {nazvanie_tovara}, {brand}, {sku}"
    keywords_element.clear()  # Очищаем поле перед вводом нового значения
    keywords_element.send_keys(keywords_value)  # Вставляем данные

    #time.sleep(100)
def main():
    # Вход в админ-панель и получение токена пользователя
    token = login()
    if token:
        print(f"Успешный вход. Токен пользователя: {token}")
        # Поиск товара по названию
        search_product_by_name(token, product_name)
    else:
        print("Не удалось войти в систему.")

if __name__ == "__main__":
    try:
        main()
        input("Нажмите Enter для выхода...")  # Держим скрипт активным, пока пользователь явно не решит выйти
    except Exception as e:
        print(f"Произошла ошибка: {e}")



