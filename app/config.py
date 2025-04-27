import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '6789'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or '6789'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    DEBUG = False
    STATIC_BEARER_TOKEN = os.environ.get('STATIC_BEARER_TOKEN') or 'default-insecure-static-token'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # SQLite en memoria para CI

config_by_name = {
    'development': Config,
    'testing': TestingConfig
}
