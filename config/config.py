# core/config.py
from my_settings import database


class Settings:
    DATABASE = f'mysql+pymysql://{database["DB_USERNAME"]}:{database["DB_PASSWORD"]}@{database["DB_HOST"]}:{database["DB_PORT"]}/{database["DB_DATABASE"]}?charset=utf8'


settings = Settings()
