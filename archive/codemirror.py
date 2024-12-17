from selenium.webdriver.common.action_chains import ActionChains

# Переключаемся в режим кода
codeview_button.click()
time.sleep(1)  # Подождите, пока режим кода активируется

# Попробуйте найти элемент текстового поля CodeMirror
code_mirror = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.CodeMirror"))
)

# Кликаем внутри CodeMirror, чтобы активировать курсор
ActionChains(driver).click(code_mirror).perform()

# Находим элемент, который активно отображает код в CodeMirror
code_mirror_textarea = driver.find_element(By.CSS_SELECTOR, "div.CodeMirror textarea")

# Вводим текст
code_mirror_textarea.send_keys(html_content)

# Возвращаемся обратно из режима кода
codeview_button.click()
time.sleep(5)  # Подождите, пока режим просмотра кода деактивируется

print("УСПЕХ, ТЕКСТ ИЗ ГПТ ВСТАВЛЕН")
