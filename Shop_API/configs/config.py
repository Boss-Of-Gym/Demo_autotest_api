"""
Конфигурационный файл для API автотестов.
Содержит настройки окружений и учетные данные для авторизации.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

APP_ENV = os.getenv("APP_ENV", "v29")
env_file = f".env.{APP_ENV}"
load_dotenv(dotenv_path=env_file)

class Config():

    BASE_DIR = Path(__file__).resolve().parent.parent
    APP_ENV = APP_ENV
    BASE_URL = os.getenv("BASE_URL")
    UUID = os.getenv("UUID")
    PLATFORM = os.getenv("PLATFORM")
    MANUFACTURER = os.getenv("MANUFACTURER")
    LANGUAGE = os.getenv("LANGUAGE")
    PROJECT = os.getenv("PROJECT")
    CHAIN = os.getenv("CHAIN")
    BRANCH = os.getenv("BRANCH")
    TOKEN_AUTHORIZATION = os.getenv("TOKEN_AUTHORIZATION")
    USER_AGENT = os.getenv("USER_AGENT")
    LOGIN_COURIER = os.getenv("LOGIN_COURIER")
    PASSWORD_COURIER = os.getenv("PASSWORD_COURIER")
    TOKEN_DEVICE = os.getenv("TOKEN_DEVICE")