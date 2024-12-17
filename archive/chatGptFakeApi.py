def chatgpt_fake_api(nazvanie_tovara, brand, sku):
    print("chatgpt_fake_api(nazvanie_tovara, brand, sku)")
    """Должна отдавать Html код"""
    # Подключаем базовый файл промпта
    with open('prompt.txt', 'r', encoding='utf-8') as file:
        prompt_file = file.read()
    prompt_to_gpt = prompt_file.format(name=nazvanie_tovara, brand=brand, sku=sku)

    # Открытие новой вкладки и переход на нее
    main_window_handle = driver.current_window_handle
    print("main_window_handle = driver.current_window_handle")
    driver.execute_script("window.open();")  # Открывает новую вкладку
    print("driver.execute_script(window.open();)")
    new_window_handle = driver.window_handles[-1]
    print("new_window_handle = driver.window_handles[-1]")
    driver.switch_to.window(new_window_handle)  # Переключается на новую вкладку
    print("driver.switch_to.window(new_window_handle)")
    # Строим URL для перехода на страницу каталога товаров с использованием токена пользователя
    driver.get("https://chat.openai.com")
    time.sleep(4)
    print("driver.get(https://chat.openai.com)")
    ##############################################################################
    #работаем с ChatGpt

    # Используем find_elements для уточнения использоваемой версии GPT, Должна быть 4
    # time.sleep(5) # поменять на явное ожидание

    try:
        wait = WebDriverWait(driver, 10)
        # xpath_query = "//div[starts-with(@id, 'radix-:ra:') or starts-with(@id, 'radix-:r5a:') or starts-with(@id, 'radix-:rd:')]/descendant::div[contains(., 'ChatGPT') and .//span[@class='text-token-text-secondary' and text()='4']]"
        # ищем среди всех радиксов
        xpath_query = "//div[starts-with(@id, 'radix-:')]/descendant::div[contains(., 'ChatGPT') and .//span[@class='text-token-text-secondary' and text()='4']]"
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_query)))
        print("wait.until(EC.presence_of_element_located((By.XPATH, xpath_query)))")
    except:
        print("Пробуем еще раз, обновляем страницу")
        #driver.get("https://chat.openai.com")
        driver.refresh()
        time.sleep(4)
        wait = WebDriverWait(driver, 10)
        xpath_query = "//div[starts-with(@id, 'radix-:ra:') or starts-with(@id, 'radix-:r5a:') or starts-with(@id, 'radix-:rd:')]/descendant::div[contains(., 'ChatGPT') and .//span[@class='text-token-text-secondary' and text()='4']]"
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_query)))
        print("wait.until(EC.presence_of_element_located((By.XPATH, xpath_query)))")
    finally:
        print("Пробуем третий раз, обновляем страницу")
        #driver.get("https://chat.openai.com")
        driver.refresh()
        time.sleep(4)
        wait = WebDriverWait(driver, 10)
        xpath_query = "//div[starts-with(@id, 'radix-:ra:') or starts-with(@id, 'radix-:r5a:') or starts-with(@id, 'radix-:rd:')]/descendant::div[contains(., 'ChatGPT') and .//span[@class='text-token-text-secondary' and text()='4']]"
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_query)))
        print("wait.until(EC.presence_of_element_located((By.XPATH, xpath_query)))")
    # После ожидания нахождение элементов
    elements = driver.find_elements(By.XPATH, xpath_query)
    time.sleep(1)
    print("elements = driver.find_elements(By.XPATH, xpath_query)")
    # Проверяем, существуют ли элементы
    if len(elements) > 0:
        print("GPT 4")
        driver.find_element(By.ID, "prompt-textarea").send_keys(prompt_to_gpt)

        sent_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="send-button"]')))
        time.sleep(10)
        #sent_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="send-button"]')
        sent_button.click()
        #ожидаем загрузки текста в элементе <code>
        code_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,"//code[contains(@class, '!whitespace-pre') and contains(@class, 'hljs')]")))
        print("Текст в элементе:", code_element.text)
        #button = driver.find_element(By.CSS_SELECTOR, 'button.flex.gap-1.items-center')
        buttons = driver.find_elements(By.CSS_SELECTOR, 'button.flex.gap-1.items-center')

        def text_to_be_present_in_element_longer_than(locator, minimum_length):
            def _predicate(driver):
                try:
                    element_text = driver.find_element(*locator).text
                    return len(element_text) > minimum_length
                except:
                    return False
            return _predicate

        # Ожидание, пока текст в элементе <code> не станет длиннее 600 символов (можете настроить длину)
        print("Ждем пока текст допишется")

        def wait_for_text_growth(driver, locator, initial_wait=60, poll_interval=8, initial_length=200):
            # Ожидание, пока текст не достигнет минимальной длины
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

            # Цикл ожидания роста длины текста
            while True:
                time.sleep(poll_interval)  # Ожидание перед следующей проверкой
                current_length = len(driver.find_element(*locator).text)

                if current_length > previous_length:
                    print(f"Длина текста увеличилась с {previous_length} до {current_length}. Продолжаем ожидание.")
                    previous_length = current_length
                else:
                    print("Длина текста не изменилась.")
                    break

        # Запуск функции ожидания роста текста
        wait_for_text_growth(driver, (By.XPATH, "//code[contains(@class, '!whitespace-pre') and contains(@class, 'hljs')]"))
        print("Текст дописан")
        code_element = driver.find_element(By.XPATH,"//code[contains(@class, 'whitespace-pre') and contains(@class, 'hljs')]")
        print("Текст в элементе:", code_element.text)
        print("Текст дописан и получен")

        # Проверка, что список кнопок не пуст, и нажатие на последнюю кнопку в списке
        if buttons:
            last_button = buttons[-1]  # Получение последней кнопки из списка
            # нажимаем на кнопку копирования
            last_button.click()
            product_description = pyperclip.paste()
            print("Текст скопирован в буфер")
        else:
            print("Кнопки с заданными классами не найдены на странице.")
            product_description = ""
        #button.click()

    else:
        print("GPT 3.5")
        product_description = ""
        print("done")
    time.sleep(1)
    ##############################################################################
    # После выполнения необходимых действий закрываем новую вкладку
    driver.close()
    driver.switch_to.window(main_window_handle)
    return product_description