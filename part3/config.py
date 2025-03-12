import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")  # Par défaut SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ta_base.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class ProductionConfig(Config):
    DEBUG = False
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
