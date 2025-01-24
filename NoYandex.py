import requests

API_URL = "https://api.direct.yandex.com/json/v5/campaigns"
TOKEN = "y0_AgAAAAAF_OAVAAyilQAAAAEVCD2dAAB43Kgwq4BAaoBzK38VVzykQ19atg"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept-Language": "ru",
    "Content-Type": "application/json",
}


def get_campaigns():
    body = {
        "method": "get",
        "params": {
            "SelectionCriteria": {},  # Получение всех кампаний
            "FieldNames": ["Id", "Name", "State"]  # Поля для вывода
        }
    }

    response = requests.post(API_URL, json=body, headers=headers)

    if response.status_code == 200:
        print("Запрос выполнен успешно!")
        return response.json()
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")
        print(response.json())


campaigns = get_campaigns()
if campaigns:
    print("Список кампаний:")
    for campaign in campaigns['result']['Campaigns']:
        print(f"ID: {campaign['Id']}, Name: {campaign['Name']}, State: {campaign['State']}")
