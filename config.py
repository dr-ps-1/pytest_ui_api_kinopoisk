import os
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)


class Config:
    """Конфигурация проекта.
    Все ключи и URL берутся из переменных окружения."""

    UI_BASE_URL: str = os.getenv('UI_BASE_URL', 'https://www.kinopoisk.ru')

    API_BASE_URL: str = os.getenv('API_BASE_URL', 'https://api.kinopoisk.dev')
    API_KEY: str = os.getenv('API_KEY', '')

    TEST_USER_EMAIL: str = os.getenv('TEST_USER_EMAIL', '')
    TEST_USER_PASSWORD: str = os.getenv('TEST_USER_PASSWORD', '')
    TEST_USER_NAME: str = os.getenv('TEST_USER_NAME', '')

    @classmethod
    def validate(cls):
        """Проверка, что все критичные переменные окружения заданы"""
        missing = []
        for attr in ['API_KEY', 'UI_BASE_URL', 'API_BASE_URL']:
            if not getattr(cls, attr):
                missing.append(attr)
        if missing:
            raise EnvironmentError(
                f"Не заданы переменные окружения: {', '.join(missing)}")


Config.validate()
