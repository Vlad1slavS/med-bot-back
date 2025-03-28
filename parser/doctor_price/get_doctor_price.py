from typing import Any

import requests
import json
import os
from dotenv import load_dotenv
from Utils.GigachatUtils import get_token

load_dotenv()
TOKEN = os.getenv("GIGACHAT_API_KEY")

# URL для загрузки файлов и для запроса чата
UPLOAD_URL = "https://gigachat.devices.sberbank.ru/api/v1/files"
CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

# Файл, который нужно передать (например, JSON с данными прайс-листа)
FILE_PATH = "../price_list.json"


# Шаг 1. Загружаем файл в GigaChat, чтобы получить file_id
def upload_file(file_path: str) -> tuple[Any, Any]:

    response = get_token(TOKEN)
    response_data = response.json()
    auth_token = response_data['access_token']

    payload = {"purpose": "general"}
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/json")}
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.post(UPLOAD_URL, headers=headers, data=payload, files=files, verify=False)
        response.raise_for_status()
        # Предположим, API возвращает JSON с ключом "id"
        file_id = response.json().get("id")
        if not file_id:
            raise ValueError("Не удалось получить file_id")
        return file_id, auth_token


# Шаг 2. Отправляем запрос в GigaChat с промптом и attachment
def get_command_from_gigachat_with_file(text: str, file_id: str):
    prompt = (
        f"Извлеки данные из файла, где в поле Name присутствует {text} "
        f"Если таких данных нет, верни пустые поля для соответствующих ключей. "
        f"Ответ должен содержать только JSON."
    )

    payload = {
        "model": "GigaChat",  # Название используемой модели (проверьте актуальное название)
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "attachments": [file_id]
            }
        ],
        "stream": False,
        "update_interval": 0,
        "max_tokens": 512
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(CHAT_URL, headers=headers, data=json.dumps(payload), verify=False)
    response.raise_for_status()
    return response.json()

#
# if __name__ == "__main__":
#     try:
#         # Пример промпта
#         prompt = (
#             "Извлеки данные из файла, где в поле Name присутствует врач-педиатр. "
#             "Если таких данных нет, верни пустые поля для соответствующих ключей. "
#             "Ответ должен содержать только JSON."
#         )
#         # Шаг 1. Загружаем файл и получаем file_id
#         file_id = upload_file(FILE_PATH)
#         print(f"Файл загружен, file_id: {file_id}")
#
#         # Шаг 2. Отправляем запрос с промптом и file_id
#         result = get_command_from_gigachat_with_file(text, file_id)
#         print("Ответ от GigaChat:")
#         print(json.dumps(result, ensure_ascii=False, indent=2))
#     except Exception as e:
#         print("Ошибка:", e)
