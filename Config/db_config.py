from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    gigachat_api_key: str  # Добавьте эту строку

    class Config:
        env_file = "../.env"  # Убедитесь, что указано правильное имя файла с переменными окружения

settings = Settings()
