from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# Настройки для использования профиля пользователя Chrome
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/0verlay/AppData/Local/Google/Chrome/User Data")  # Путь к профилю
options.add_argument("profile-directory=Profile 1")  # Имя профиля
options.add_argument("--disable-blink-features=AutomationControlled") #Скрываем Webdriver
options.headless = False  # Убедитесь, что headless режим отключен, если хотите видеть UI
driver = webdriver.Chrome(options=options)


# Открываем браузер на полный экран
driver.maximize_window()

# Переход на другой URL
driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")

# Демонстрационная задержка
time.sleep(5)  # Используйте явные ожидания

# Закрываем браузер
driver.quit()