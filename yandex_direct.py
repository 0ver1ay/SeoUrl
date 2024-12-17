from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time


def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=E:\\WORK\\Python\\SeoScraper\\chromeCache")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('user-data-dir=C:/Users/0verlay/AppData/Local/Google/Chrome/User Data')
    chrome_options.add_argument('profile-directory=Profile 1')
    chrome_options.headless = False

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver


def scroll_to_show_elements(driver, current_element, previous_element):
    # Прокручиваем к предыдущему элементу
    driver.execute_script("arguments[0].scrollIntoView(true);", previous_element)
    # Прокручиваем немного вниз, чтобы текущий элемент был в поле зрения
    driver.execute_script("window.scrollBy(0, 100);")


def process_page(driver, url):
    driver.get(url)

    total_processed = 0  # Счетчик для общего числа обработанных элементов

    while True:
        try:
            # Получаем видимые элементы заново
            visible_elements = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "phrase-money-cell-editor"))
            )
            visible_elements = [elem for elem in visible_elements if elem.is_displayed()]

            total_count = len(visible_elements)
            print(f"Найдено видимых элементов: {total_count}")

            if total_count == 0:
                print("Нет видимых элементов для обработки.")
                break

            # Обрабатываем все видимые элементы
            for index in range(total_count):
                try:
                    current_element = visible_elements[index]

                    # Прокрутка к текущему элементу
                    driver.execute_script("arguments[0].scrollIntoView(true);", current_element)
                    time.sleep(0.5)  # Пауза, чтобы элемент стал кликабельным

                    # Убедитесь, что элемент видим и кликабелен
                    WebDriverWait(driver, 10).until(EC.visibility_of(current_element))
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(current_element))

                    # Закрытие всплывающего окна, если оно есть
                    try:
                        popup = WebDriverWait(driver, 0.5).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "dc-PopupConfirm__content-wrapper"))
                        )
                        close_button = popup.find_element(By.XPATH, "//button[contains(@class, 'close-button')]")
                        close_button.click()
                        time.sleep(0.5)
                    except:
                        pass

                    # Клик по текущему элементу
                    driver.execute_script("arguments[0].click();", current_element)
                    time.sleep(0.5)

                    # Ждем появления всплывающего окна
                    popup = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "dc-Island"))
                    )

                    div_element = popup.find_element(By.CLASS_NAME, "phrase-traffic-forecast__input")
                    input_field = div_element.find_element(By.CSS_SELECTOR, "input.Textinput-Control")

                    # Очищаем текущее значение
                    input_field.send_keys(Keys.CONTROL + "a")
                    input_field.send_keys(Keys.DELETE)

                    # Вводим новое значение — '85'
                    input_field.send_keys("85")

                    # Находим кнопку "Сохранить" и кликаем по ней
                    save_button = popup.find_element(By.XPATH, "//span[contains(text(), 'Сохранить')]")
                    save_button.click()
                    time.sleep(0.5)

                    total_processed += 1  # Увеличиваем счетчик обработанных элементов
                    print(f"Обработан элемент {index + 1} из {total_count}. Всего обработано: {total_processed}.")

                except StaleElementReferenceException:
                    print("Ссылка на элемент устарела, повторная попытка...")
                    # Получаем элементы заново
                    visible_elements = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "phrase-money-cell-editor"))
                    )
                    visible_elements = [elem for elem in visible_elements if elem.is_displayed()]
                    break  # Выход из внутреннего цикла, чтобы начать заново

            # Проверяем еще раз, есть ли видимые элементы после обработки
            visible_elements = [elem for elem in driver.find_elements(By.CLASS_NAME, "phrase-money-cell-editor") if elem.is_displayed()]
            if not visible_elements:
                print("Нет больше видимых элементов для обработки.")
                break

        except TimeoutException:
            print("Время ожидания истекло. Пожалуйста, проверьте страницу.")
            break

    print(f"Обработка завершена. Всего обработано элементов: {total_processed}.")


def main():
    driver = setup_driver()

    # Список ссылок, которые нужно обработать
    urls = [
        "https://direct.yandex.ru/dna/grid/phrases?ulogin=test-login&stat-preset=last30Days&tags=&filter=%D0%A1%D1%82%D0%B0%D1%82%D1%83%D1%81%20%3D%20%D0%92%D1%81%D0%B5%20%D1%84%D1%80%D0%B0%D0%B7%D1%8B",
    ]

    for url in urls:
        process_page(driver, url)

    driver.quit()


if __name__ == "__main__":
    main()
