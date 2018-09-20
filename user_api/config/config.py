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
    SECRET_KEY = '38c59ca136a64ae994153a015dbb6519e71ebacc331b85ba'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    HOST = "127.0.0.1"
    PORT = "5432"
    DATABASE = "user_api_db"
    DATABASE_URL = 'postgres://imxhfeqifoestz:689239e3f43d0bd11484b9dcc049e7ba3beed97f1f192dc49b5df388f43af2cd@ec2-54' \
                   '-225-97-112.compute-1.amazonaws.com:5432/d80tbmd64eh4km '
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
    SECRET_KEY = '38c59ca136a64ae994153a015dbb6519e71ebacc331b85ba'
    DEBUG = False
    SCHEMA_PRODUCTION = "production"