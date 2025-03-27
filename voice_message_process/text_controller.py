import logging

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from voice_message_process import gigachat
from voice_message_process.audio_to_text_service import transcribe_audio

router = APIRouter()


class TextRequest(BaseModel):
    text: str


@router.post("/process_audio")
async def process_voice(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    text = transcribe_audio(file_location)
    response = gigachat.get_chat_completion(text)  # Получаем Response

    try:
        command = response.json()  # Преобразуем в JSON
    except Exception as e:
        return {"error": f"Ошибка обработки JSON: {str(e)}"}

    print(command)
    return {"command": command}

