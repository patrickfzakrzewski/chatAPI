import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))


class Config:
    DEBUG = False
    SECRET_KEY = 'thisisthesecretkey'
    JSON_SORT_KEYS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'chatAPI.db')
