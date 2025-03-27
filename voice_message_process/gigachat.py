import os
from dotenv import load_dotenv
import requests
import json
import uuid


load_dotenv()

TOKEN = os.getenv("GIGACHAT_API_KEY")

COMMANDS = ["запись", "отмена записи", "цена", "маршрут"]

def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {
        'scope': scope
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1

def get_chat_completion(user_message):
    content = (
        f"Обработай голосовое сообщение пользователя: \"{user_message}\" "
        f"и верни JSON с подходящей командой. Доступные команды: {COMMANDS}. "
        f"\n\nПравила формирования ответа:"
        f"\n1. Если это команда записи, верни JSON с ключами: 'command' (команда), 'doctor' (врач), 'date' (дата (день, месяц) без года!), 'time' (время)."
        f"\n2. Если уточняется стоимость, верни JSON с ключами: 'command' ('цена') и 'service' (процедура или врач)."
        f"\n3. Если данные неясны, оставь соответствующие поля пустыми."
        f"\n4. Исправляй ошибки в тексте."
        f"\n5. Ответ должен содержать только JSON, без поясняющего текста."
    )

    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    response = get_token(TOKEN)
    response_data = response.json()
    auth_token = response_data['access_token']

    # Подготовка данных запроса в формате JSON
    payload = json.dumps({
        "model": "GigaChat-Max",  # Используемая модель
        "messages": [
            {
                "role": "user",  # Роль отправителя (пользователь)
                "content": content  # Содержание сообщения
            }
        ],
        "temperature": 1,  # Температура генерации
        "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,  # Потоковая ли передача ответов
        "max_tokens": 512,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1,  # Штраф за повторения
        "update_interval": 0  # Интервал обновления (для потоковой передачи)
    })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {auth_token}'  # Токен авторизации
    }

    # Выполнение POST-запроса и возвращение ответа
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return -1