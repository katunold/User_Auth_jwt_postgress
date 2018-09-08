"""
Module contains all global constants
"""
import os


class HostConfig:
    """
    System HOST configuration settings
    They can be changed at any time.
    """
    HOST = "0.0.0.0"
    PORT = 5000


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', '\xf3G/y\xa4\xf0\x84(\x11\x16i\xb7\xb6\xfb\xdd\x11\x88\x12\x92V;\x0c`{')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    HOST = "127.0.0.1"
    PORT = "5432"
    DATABASE = "user_api_db"
    USER = "postgres"
    PASSWORD = "qwerty"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SCHEMA_PRODUCTION = "production"


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SCHEMA_TESTING = "tests"


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = '\xf3G/y\xa4\xf0\x84(\x11\x16i\xb7\xb6\xfb\xdd\x11\x88\x12\x92V;\x0c`{'
    DEBUG = False
    SCHEMA_PRODUCTION = "production"