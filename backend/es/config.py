import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    pass


class Config(BaseConfig):
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWD = os.environ.get("DB_PASSWD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
