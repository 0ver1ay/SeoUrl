import re


def format_product_name_old(product_name):
    # Список моделей Рено и Лады
    renault_models = ["Логан", "Сандеро", "Лагуна", "Дастер", "Каптур", "Флюенс", "Аркана", "Клио", "Кангу", "Колеос",
                      "Трафик", "Мастер", "Меган", "Сценик", "Симбол", "Талисман", "Эспейс", "Эспейс", "Маскотт", "Доккер"]
    lada_models = ["Ларгус"]
    peugeot_models = ["Партнер", "106", "107", "1007", "206", "207", "208", "301", "306", "307", "308", "406", "407", "408", "2008", "3008",
                      "4007",
                      "4008", "5008", "Партнер", "Эксперт", "Боксер", "Тревеллер"]
    citroen_models = ["С1", "C1", "C2", "С2", "С3", "С3 Пикассо", "С4", "С5", "C5", "С4 Пикассо", "С3", "C3", "C3 Пикассо",
                      "С3 Пикассо", "C4",
                      "C4 Пикассо", "C4 Пикассо", "Спейстурер", "С-Кроссер", "С-Элизи", "Берлинго",
                      "Джампи", "Джампер"]
    nissan_models = ["Террано", "Альмера"]

    # Функция для добавления названия бренда к модели
    def add_brand(model, brand):
        return f"{brand} {model}"

    # Проверяем каждую модель в списке моделей Рено
    for model in renault_models:
        if model in product_name:
            product_name = product_name.replace(model, add_brand(model, "Рено"), 1)
            break  # Прерываем цикл после первой замены

    # Проверяем каждую модель в списке моделей Лады
    for model in lada_models:
        if model in product_name:
            product_name = product_name.replace(model, add_brand(model, "Лада"), 1)
            break  # Прерываем цикл после первой замены

    # Проверяем каждую модель в списке моделей Рено
    for model in peugeot_models:
        if model in product_name:
            product_name = product_name.replace(model, add_brand(model, "Пежо"), 1)
            break  # Прерываем цикл после первой замены

    for model in citroen_models:
        if model in product_name:
            product_name = product_name.replace(model, add_brand(model, "Ситроен"), 1)
            break  # Прерываем цикл после первой замены

    for model in nissan_models:
        if model in product_name:
            product_name = product_name.replace(model, add_brand(model, "Ниссан"), 1)
            break  # Прерываем цикл после первой замены

    return product_name


def add_brand_to_product(product_name):
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
        "С4": "Ситроен", "С5": "Ситроен", "C5": "Ситроен", "С4 Пикассо": "Ситроен", "C3": "Ситроен",
        "C3 Пикассо": "Ситроен", "С3 Пикассо": "Ситроен", "C4": "Ситроен", "C4 Пикассо": "Ситроен",
        "C4 Пикассо": "Ситроен", "Спейстурер": "Ситроен", "С-Кроссер": "Ситроен", "С-Элизи": "Ситроен",
        "Берлинго": "Ситроен", "Джампи": "Ситроен", "Джампер": "Ситроен",
        "Террано": "Ниссан", "Альмера": "Ниссан"
    }

    # Регулярное выражение для поиска моделей
    model_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(model) for model in models_brands.keys()) + r')(?=[.,/\s]|$)')

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

# Пример использования функции
product_name = "Пыльник ШРУСа наружний Кангу 2/Сандеро Степвей/Логан 2/Партнер/Берлинго"
output = add_brand_to_product(product_name)
print(output)

