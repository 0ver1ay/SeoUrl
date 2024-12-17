import time

from selenium import webdriver
import json

# Путь к вашему драйверу и файлу cookies
options = webdriver.ChromeOptions()
options.headless = False  # Убедитесь, что headless режим отключен, если хотите видеть UI
driver = webdriver.Chrome(options=options)
driver.maximize_window()  # Добавляем эту строку для открытия браузера на полный экран
cookies_path = 'cookies.json'

# Открытие страницы (необходимо для установки cookies)
driver.get("http://chat.openai.com")



# Загрузка cookies из файла
with open(cookies_path, 'r') as cookies_file:
    cookies = json.load(cookies_file)

# Добавление каждого cookie в сеанс WebDriver
# Обработка и добавление каждого cookie
for cookie in cookies:
    cookie.pop('hostOnly', None)  # Удаление неиспользуемых полей
    cookie.pop('session', None)
    cookie.pop('storeId', None)
    cookie.pop('id', None)

    if 'expirationDate' in cookie:
        cookie['expiry'] = int(cookie.pop('expirationDate'))  # Преобразуем expirationDate в expiry

    if 'sameSite' in cookie:
        if cookie['sameSite'] == 'no_restriction':
            cookie['sameSite'] = 'None'  # Исправляем значение sameSite

# Перезагрузка страницы с новыми cookies
driver.get("http://chat.openai.com")
time.sleep(1000)