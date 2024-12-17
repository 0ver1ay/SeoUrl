from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from collections import deque
from functools import wraps
import pyperclip
import time
import datetime
import re
import logging

# Настройка логирования
logging.basicConfig(filename='app.log',  # Имя файла лога
                    filemode='a',  # Режим открытия файла, 'a' означает дозапись
                    format='%(name)s - %(levelname)s - %(message)s',  # Формат сообщения
                    level=logging.WARNING,  # Уровень логирования
                    encoding='utf-8')  # Кодировка

# Параметры для входа в систему
base_url = "https://renokom.ru/admin/"
username = "bender"
password = "L$@56###4h2%2^^^1xs!*uU"

# Искать конкретный товар
# "Сальник", - как поправим в 1с
product_names = [
    "Эмблема"
]


# Настройки для использования профиля пользователя Chrome
options = webdriver.ChromeOptions()

# Прячемся от капч
options.add_argument("--disable-blink-features=AutomationControlled")  # Скрываем Webdriver, чтобы не проходить капчу
# For older ChromeDriver under version 79.0.3945.16
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# For ChromeDriver version 79.0.3945.16 or over
options.add_argument('--disable-blink-features=AutomationControlled')
# Открывает Chrome с текущими настройками профиля, чтобы не вводить капчи
options.add_argument("user-data-dir=C:/Users/0verlay/AppData/Local/Google/Chrome/User Data")  # Путь к профилю
options.add_argument("profile-directory=Profile 1")  # Имя профиля

options.headless = False  # Убедитесь, что headless режим отключен, если хотите видеть UI
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Если остались какие-то открытые вкладки, закроет их
# Сохранение идентификатора первой вкладки
first_tab = driver.window_handles[0]
# Закрытие всех вкладок, кроме первой
for handle in driver.window_handles:
    if handle != first_tab:
        driver.switch_to.window(handle)
        driver.close()
# Переключение обратно на первую вкладку
driver.switch_to.window(first_tab)


# __________________________________________________

def setup_old_driver():
    options = webdriver.ChromeOptions()
    options.headless = False  # Убедитесь, что headless режим отключен, если хотите видеть UI
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()  # Добавляем эту строку для открытия браузера на полный экран

def login():
    """ Функция для входа в админ-панель OpenCart. """
    try:
        driver.get(base_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
        time.sleep(2)
        # если не используем готовый профиль, то придетя вводить пароль
        # driver.find_element(By.ID, "input-username").send_keys(username)
        # driver.find_element(By.ID, "input-password").send_keys(password)

        driver.find_element(By.CLASS_NAME, "btn-primary").click()

        # Ожидаем редиректа на главную страницу админ-панели и извлекаем user_token
        WebDriverWait(driver, 10).until(EC.url_contains("route=common/dashboard"))
        current_url = driver.current_url
        token_match = re.search(r'user_token=([^&]+)', current_url)
        return token_match.group(1) if token_match else None
    except Exception as e:
        print(f"Ошибка входа: {e}")
        return None

def format_product_name(product_name):
    # Словарь моделей и их брендов
    models_brands = {
        "Логан": "Рено", "Сандеро": "Рено", "Лагуна": "Рено", "Дастер": "Рено", "Каптур": "Рено", "Флюенс": "Рено",
        "Аркана": "Рено", "Клио": "Рено", "Кангу": "Рено", "Колеос": "Рено", "Трафик": "Рено", "Мастер": "Рено",
        "Меган": "Рено", "Сценик": "Рено", "Симбол": "Рено", "Талисман": "Рено", "Эспейс": "Рено", "Маскотт": "Рено",
        "Доккер": "Рено",
        "Ларгус": "Лада",
        "Партнер": "Пежо", "106": "Пежо", "107": "Пежо", "1007": "Пежо", "206": "Пежо", "207": "Пежо", "208": "Пежо",
        "301": "Пежо", "306": "Пежо", "307": "Пежо", "308": "Пежо", "406": "Пежо", "407": "Пежо", "408": "Пежо",
        "2008": "Пежо", "3008": "Пежо", "4007": "Пежо", "4008": "Пежо", "5008": "Пежо", "Эксперт": "Пежо",
        "Боксер": "Пежо", "Тревеллер": "Пежо",
        "С1": "Ситроен", "C1": "Ситроен", "C2": "Ситроен", "С2": "Ситроен", "С3": "Ситроен", "С3 Пикассо": "Ситроен",
        "С4": "Ситроен", "С5": "Ситроен", "C5": "Ситроен", "C3": "Ситроен",
        "C3 Пикассо": "Ситроен", "C4": "Ситроен", "С4 Пикассо": "Ситроен",
        "C4 Пикассо": "Ситроен", "Спейстурер": "Ситроен", "С-Кроссер": "Ситроен", "С-Элизи": "Ситроен",
        "Берлинго": "Ситроен", "Джампи": "Ситроен", "Джампер": "Ситроен",
        "Террано": "Ниссан", "Альмера": "Ниссан"
    }

    # Регулярное выражение для поиска моделей
    model_pattern = re.compile(
        r'\b(?:' + '|'.join(re.escape(model) for model in models_brands.keys()) + r')(?=[.,/\s]|$)')

    # Набор для отслеживания уже добавленных марок
    added_brands = set()

    def replace_model(match):
        model = match.group(0)
        brand = models_brands[model]
        if brand not in added_brands:
            added_brands.add(brand)
            return brand + " " + model
        return model

    # Замена моделей на марки в строке
    output = model_pattern.sub(replace_model, product_name)
    return output

def search_product_by_name(token, product_names):
    #print("search_product_by_name()")
    """Функция для поиска товара по названию в админ-панели OpenCart."""
    "Храним данные о последнем обработанном товаре, если программа упадет"
    "если в файле, где храним оем пусто, то все ок, если что-то есть, начинаем считать с него"
    for product_name in product_names:
        try:
            category_window_handle = driver.current_window_handle
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
            time.sleep(2)
            #print("Поиск выполнен. Начинаем обработку каждого товара.")

            # Открываем каждый товар в новой вкладке и выполняем действия

            open_each_product_in_new_tab()
            time.sleep(1)
            # driver.close()
        finally:
            pass
    #print("search_product_by_name(x)")

def open_each_product_in_new_tab():
    #print("open_each_product_in_new_tab()")
    """Функция для открытия каждого товара в новой вкладке и выполнения действий на них."""
    category_window_handle = driver.current_window_handle
    try:
        #print("open_each_product_in_new_tab()")
        product_links = driver.find_elements(By.CSS_SELECTOR,
                                             "a.btn-primary[data-toggle='tooltip'][data-original-title='Редактировать']")
        # print("Элементы найдены")
        #main_window_handle = driver.current_window_handle
        for link in product_links:
            # print(link.get_attribute('href'))
            product_url = link.get_attribute('href')
            # Убедитесь, что URL содержит нужный user_token
            # print(f"Открываем URL товара: {product_url}")  # Для отладки

            driver.execute_script("window.open();")  # Открывает новую вкладку
            new_window_handle = driver.window_handles[-1]
            driver.switch_to.window(new_window_handle)  # Переключается на новую вкладку
            driver.get(product_url)  # Переходит на страницу товара
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".chatgptseo-refresh")))
            # Выполнение действий на странице товара
            perform_actions_and_save_product()
            time.sleep(1)
            driver.switch_to.window(category_window_handle)
    except:
        driver.switch_to.window(category_window_handle)
    finally:
        #print("Закрываем все вкладки, кроме вкладки категорий")
        # закрытие всех вкладок кроме категорий
        all_handles = driver.window_handles
        for handle in all_handles:
            if handle != category_window_handle:
                driver.switch_to.window(handle)
                driver.close()
    #print("open_each_product_in_new_tab(x)")

def check_product_validity():
    #print("check_product_validity()")
    general_link = driver.find_element(By.CSS_SELECTOR, "a[href='#tab-data']")
    textarea = driver.find_element(By.NAME, "quantity")
    quantity = int(textarea.get_attribute("value"))
    # Найти элемент <select> по его ID или классу
    select_element = driver.find_element(By.ID, "input-status")

    # Инициализируем объект Select, используя найденный элемент
    select = Select(select_element)

    # Получаем выбранный в данный момент элемент <option>
    selected_option = select.first_selected_option

    # Получаем значение или текст выбранного элемента
    selected_text = selected_option.get_attribute("text")
    # print("количество = " + str(quantity) + ", статус = " + selected_text)

    if quantity != 0 and selected_text == "Включено":
        general_link = driver.find_element(By.CSS_SELECTOR, "a[href='#tab-general']")
        general_link.click()
        # logging.warning("Количество товара = " + str(quantity) + ", Товар включен")
        #print("Количество товара = " + str(quantity) + ", Товар включен")
        #print("check_product_validity(x)")
        return True
    else:
        #print("check_product_validity(x)")
        return False

def perform_actions_and_save_product():
    #print("perform_actions_and_save_product()")
    """Функция для выполнения действий на странице товара, сохранения изменений и ожидания подтверждения."""
    "Проверка, что количество товара > 0"
    if check_product_validity():
        "Меняем все параметры товара"
        isValid = True
        change_product(isValid)
    else:
        "Меняем только метатеги"
        isValid = False
        change_product(isValid)
    # time.sleep(10000)
    # Находим кнопку сохранения и кликаем по кнопке "Сохранить"
    time.sleep(2)
    save_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][form='form-product']")
    save_button.click()
    # Ожидаем, пока не появится элемент, сигнализирующий о том, что изменения сохранены
    #(print("Ожидаем, пока не появится элемент, сигнализирующий о том, что изменения сохранены"))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "button-filter")))
    #(print("Изменения сохранены, закрываем вкладку товара"))
    # Элемент появился, изменения сохранены, можно закрывать вкладку
    driver.close()
    time.sleep(1)
    #print("perform_actions_and_save_product(x)")

def change_product(isValid):
    #print("change_product(isValid)")
    #print("change_product(isValid)")
    """Функция для изменения характеристик товара. h1, title, description на основе названия, артикула и производителя товара"""
    #print("Мы дошли до изменения продукта, ожидаем")
    # Находим форму для ввода нового названия товара
    input_name2 = driver.find_element(By.ID, "input-name2")
    # Получаем текст из формы
    nazvanie_tovara = input_name2.get_attribute('value')
    # Пример использования нового текста
    #print("Обработка товара:", nazvanie_tovara)
    # Переходим ко вкладке "Характеристики"
    characteristics_link = driver.find_element(By.CSS_SELECTOR, "a[href='#tab-attribute']")
    characteristics_link.click()
    # Ищем поле "Бренд"
    # textarea = driver.find_element(By.NAME, "product_attribute[0]")
    textarea = driver.find_element(By.CSS_SELECTOR, "textarea[name*='product_attribute[0]']")
    # Получаем содержимое текстового поля
    brand = textarea.get_attribute('value')
    # Переходим ко вкладке "Данные"
    dannye_link = driver.find_element(By.CSS_SELECTOR, "a[href='#tab-data']")
    dannye_link.click()
    textarea = driver.find_element(By.NAME, "sku")
    # Получаем содержимое текстового поля
    sku = textarea.get_attribute('value')
    print("Обработка товара:", nazvanie_tovara + " " + brand + " " + sku)

    # Используем полученные данные
    # Переходим ко вкладке "Общие"
    general_link = driver.find_element(By.CSS_SELECTOR, "a[href='#tab-general']")
    general_link.click()

    # Меняем названия по канону(можно отключить) ,поставив False
    if True:
        nazvanie_tovara = format_product_name(nazvanie_tovara)
    if isValid:
        # Заполняем поле описания с помощью чатгпт
        fill_metatags(nazvanie_tovara, brand, sku)
        # Заполняем поля метатегов на основе полученных данных
        fill_chatgpt(nazvanie_tovara, brand, sku)
    else:
        # Заполняем поля метатегов на основе полученных данных
        fill_metatags(nazvanie_tovara, brand, sku)
    #print("change_product(x)")
    # time.sleep(100)

def fill_metatags(nazvanie_tovara, brand, sku):
    #print("fill_metatags()")
    h1_element = driver.find_element(By.ID, "input-meta-h12")
    h1_value = f"{nazvanie_tovara} {brand} {sku}"
    h1_element.clear()  # Очищаем поле перед вводом нового значения
    h1_element.send_keys(h1_value)  # Вставляем данные

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
    #print("fill_metatags(x)")

def fill_chatgpt(nazvanie_tovara, brand, sku):
    #print("fill_chatgpt()")
    try:
        #print("fill_chatgpt(nazvanie_tovara, brand, sku)")

        # Находим элемент для редактирования
        editable_div = driver.find_element(By.CSS_SELECTOR, ".note-editable")
        product_window_handle = driver.current_window_handle
        # Проверяем длину поля с описанием, если заполнено, то не переписываем
        if len(editable_div.text) < 100:
            # Используем JavaScript для вставки HTML в содержимое редактируемого div
            html_content = ""

            html_content = chatgpt_fake_api(nazvanie_tovara, brand, sku, product_window_handle)
            if len(html_content) > 800:
                # driver.execute_script(f"arguments[0].innerHTML = `{html_content}`;", editable_div)
                editable_div = driver.find_element(By.CSS_SELECTOR, "div.note-editable.panel-body")

                # Прощелкиваем кодвью туда-обратно
                # Построение XPath для выбора третьего элемента div с классом 'form-group'
                div_xpath = "(//div[@class='form-group'])[2]"
                # Построение XPath для кнопки внутри этого div
                codeview_button_xpath = f"{div_xpath}//button[contains(@class, 'btn-codeview')]"

                # Ожидание видимости кнопки и выполнение действия
                codeview_button = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, codeview_button_xpath)))

                editable_div.click()
                time.sleep(1) # debug
                editable_div.clear()
                codeview_button.click()
                # Подождите, пока режим кода активируется
                time.sleep(2) # debug

                # Попробуйте найти элемент текстового поля CodeMirror
                code_mirror = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.CodeMirror"))
                )

                # Кликаем внутри CodeMirror, чтобы активировать курсор
                ActionChains(driver).click(code_mirror).perform()
                time.sleep(2) # debug
                # Находим элемент, который активно отображает код в CodeMirror
                code_mirror_textarea = driver.find_element(By.CSS_SELECTOR, "div.CodeMirror textarea")

                # Вводим текст
                # code_mirror_textarea.clear()
                code_mirror_textarea.send_keys(html_content)

                # Возвращаемся из режима кода
                codeview_button.click()
                time.sleep(1)  # Ждем, пока режим просмотра кода деактивируется
                print("УСПЕХ, ТЕКСТ ИЗ ГПТ ВСТАВЛЕН")
                pyperclip.copy('')
            else:
                driver.refresh()
                print("fill_chatgpt(AGAIN) - из ГПТ скопировалось короткое описание")
                fill_chatgpt(nazvanie_tovara, brand, sku)
                time.sleep(1)
        else:
            print("Описание заполнено")
    except:
        driver.refresh()
        #print("fill_chatgpt(AGAIN)")
        fill_chatgpt(nazvanie_tovara, brand, sku)
        time.sleep(1)
    finally:
        print("Переходим к следующему товару")
        print("                             ")
        #print("fill_chatgpt(x)")

def retry_on_exception(attempts=10):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Попытка получить 'product_window_handle' из kwargs или из args
            if 'product_window_handle' in kwargs:
                product_window_handle = kwargs['product_window_handle']
            else:
                try:
                    # Предполагаем, что 'product_window_handle' находится в последнем позиционном аргументе
                    product_window_handle = args[-1]
                except IndexError:
                    raise ValueError("product_window_handle was not provided as an argument.")

            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == attempts - 1:
                        raise
                    driver.close()
                    print("Handler ", product_window_handle)
                    driver.switch_to.window(product_window_handle)
                    print("Retrying the function...")
        return wrapper
    return decorator


@retry_on_exception(attempts=10)
def chatgpt_fake_api(nazvanie_tovara, brand, sku, product_window_handle):
    #print("chatgpt_fake_api()")
    timeout_attemps = 0
    product_description = ""
    while timeout_attemps < 10:
        try:
            #print("chatgpt_fake_api(nazvanie_tovara, brand, sku)")
            """Должна отдавать Html код"""
            # Подключаем базовый файл промпта
            with open('prompt.txt', 'r', encoding='utf-8') as file:
                prompt_file = file.read()
            prompt_to_gpt = prompt_file.format(name=nazvanie_tovara, brand=brand, sku=sku)
            time.sleep(1)
            # Открытие новой вкладки и переход на нее
            driver.execute_script("window.open();")  # Открывает новую вкладку
            #print("driver.execute_script(window.open();)")
            new_window_handle = driver.window_handles[-1]
            #print("new_window_handle = driver.window_handles[-1]")
            driver.switch_to.window(new_window_handle)  # Переключается на новую вкладку
            #print("driver.switch_to.window(new_window_handle)")
            # Строим URL для перехода на страницу каталога товаров с использованием токена пользователя
            driver.get("https://chat.openai.com/?model=gpt-4")
            time.sleep(4)
            print("driver.get(https://chat.openai.com/?model=gpt-4)")
            ##############################################################################
            # работаем с ChatGpt
            # Используем find_elements для уточнения использоваемой версии GPT, Должна быть 4

            wait = WebDriverWait(driver, 10)
            xpath_query = "//div[starts-with(@id, 'radix-:ra:') or starts-with(@id, 'radix-:r5a:') or starts-with(@id, 'radix-:rd:')]/descendant::div[contains(., 'ChatGPT') and .//span[@class='text-token-text-secondary' and text()='4']]"
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_query)))
            #print("wait.until(EC.presence_of_element_located((By.XPATH, xpath_query)))")
            # После ожидания нахождение элементов
            elements = driver.find_elements(By.XPATH, xpath_query)
            time.sleep(1)
            print("Проверяем версию ГПТ")
            # Проверяем, существуют ли элементы
            #print(len(elements))
            print("GPT 4")
            driver.find_element(By.ID, "prompt-textarea").send_keys(prompt_to_gpt)
            time.sleep(5)
            sent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="send-button"]')))
            time.sleep(5)
            # sent_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="send-button"]')
            sent_button.click()
            # ожидаем загрузки текста в элементе <code>
            time.sleep(5)
            try:
                code_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                    (By.XPATH, "//code[contains(@class, '!whitespace-pre') and contains(@class, 'hljs')]")))
                print("Текст генерируется")
                break
            except:
                # Находим span с указанным текстом
                span_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                                                               (By.XPATH, "//span[contains(text(),'reached the current usage cap for GPT-4')]")))
                # Выводим текст найденного элемента
                print(span_element.text)
                time_from_gpt = span_element.text
                timeout_attemps += 1

                def waiting(time_from_gpt):
                    time_pattern = r'(\d{1,2}:\d{2} [AP]M)'
                    match = re.search(time_pattern, time_from_gpt)
                    if match:
                        time_str = match.group(0)
                        print("Найдено время:", time_str)
                    else:
                        print("Время не найдено")
                        return

                    current_time = datetime.datetime.now().strftime("%I:%M %p")
                    print("Текущее время:", current_time)

                    # Convert current time and desired time to datetime objects
                    current_time_dt = datetime.datetime.strptime(current_time, "%I:%M %p")
                    desired_time_dt = datetime.datetime.strptime(time_str, "%I:%M %p")

                    # Check if desired time is in the future compared to the current time
                    if desired_time_dt <= current_time_dt:
                        print("Desired time is in the past or the same as the current time.")
                        return

                    # Calculate the time difference in seconds
                    time_diff_seconds = (desired_time_dt - current_time_dt).total_seconds()
                    print("Разница в секундах:", time_diff_seconds)

                    total_seconds = max(0, int(time_diff_seconds))  # Ensure non-negative total_seconds

                    if total_seconds > 0:
                        print("Waiting for", total_seconds, "seconds")
                        time.sleep(total_seconds)
                        print("Waited for", total_seconds, "seconds")
                    else:
                        print("No need to wait")
                # Call the waiting function after defining it
                try:
                    waiting(time_from_gpt)
                    time.sleep(120)
                finally:
                    driver.close()
                    driver.switch_to.window(product_window_handle)
                time.sleep(2)
                continue
        finally:
            time.sleep(1)
    # Ожидание, пока текст в элементе <code> не станет длиннее 600 символов (можете настроить длину)
    #print("Ждем пока текст допишется")
    # button = driver.find_element(By.CSS_SELECTOR, 'button.flex.gap-1.items-center')
    buttons = driver.find_elements(By.CSS_SELECTOR, 'button.flex.gap-1.items-center')
    def wait_for_text_growth(driver, locator, initial_wait=20, poll_interval=8, initial_length=200):
        # Ожидание, пока текст не достигнет минимальной длины
        #print("wait_for_text_growth()")
        try:
            WebDriverWait(driver, initial_wait).until(
            lambda x: len(driver.find_element(*locator).text) >= initial_length
            )
        except TimeoutException:
            print(f"Текст не достиг минимальной длины {initial_length} символов в течение {initial_wait} секунд.")
            print("длина текста = " + str(len(driver.find_element(*locator).text)))
            return False

        print(f"Текст достиг минимальной длины {initial_length} символов.")
        previous_length = len(driver.find_element(*locator).text)

        #Цикл ожидания роста длины текста
        while True:
            time.sleep(poll_interval)  # Ожидание перед следующей проверкой
            current_length = len(driver.find_element(*locator).text)

            if current_length > previous_length:
                #print(f"Длина текста увеличилась с {previous_length} до {current_length}. Продолжаем ожидание.")
                print(".", end="")
                previous_length = current_length
            else:
                print("Сгенерировано!")
                break
        #print("wait_for_text_growth(x)")
    # Запуск функции ожидания роста текста
    wait_for_text_growth(driver,
                         (By.XPATH, "//code[contains(@class, '!whitespace-pre') and contains(@class, 'hljs')]"))
    #print("Текст дописан")
    code_element = driver.find_element(By.XPATH,
                                       "//code[contains(@class, 'whitespace-pre') and contains(@class, 'hljs')]")
    print("Сгенерированный текст:", code_element.text)
    #print("Текст дописан и получен")

    # Проверка, что список кнопок не пуст, и нажатие на последнюю кнопку в списке
    if buttons:
        last_button = buttons[-1]  # Получение последней кнопки из списка
        # нажимаем на кнопку копирования
        last_button.click()
        product_description = pyperclip.paste()
        print("Текст скопирован в буфер")
    else:
        print("Кнопки с заданными классами не найдены на странице.")

    ##############################################################################
    # После выполнения необходимых действий закрываем новую вкладку
    driver.close()
    driver.switch_to.window(product_window_handle)
    #print("chatgpt_fake_api(x)")
    return product_description


def main():
    # Вход в админ-панель и получение токена пользователя
    token = login()
    if token:
        print(f"Успешный вход. Токен пользователя: {token}")
        # Поиск товара по названию
        search_product_by_name(token, product_names)
    else:
        print("Не удалось войти в систему.")


if __name__ == "__main__":
    try:
        main()
        input("Нажмите Enter для выхода...")  # Держим скрипт активным, пока пользователь явно не решит выйти
    except Exception as e:
        print(f"Произошла ошибка: {e}")
