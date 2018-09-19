"""
Authentication module for JWT token
"""
import os

import bcrypt
import datetime

import jwt

from user_api.models.token_model import Tokens
from user_api.models.user_model import Users
import user_api.run
from user_api.utils.singleton import Singleton
from user_api.models.user_model import UserModel


class Authenticate(metaclass=Singleton):
    """
    Class defines method used by JWT
    """
    __users = Users()

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generate auth token
        :param user_id:
        :return:
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            val = jwt.encode(payload, user_api.run.APP.config.get('SECRET_KEY'), algorithm='HS256')
            return val
        except Exception as ex:
            return ex

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return:
        """

        try:
            payload = jwt.decode(auth_token, user_api.run.APP.config.get('SECRET_KEY'))
            is_blacklisted_token = Tokens().check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def verify_password(password_text, hashed):
        """
        verify client password with stored password
        :param password_text:
        :param hashed:
        :return:
        """
        try:
            return bcrypt.checkpw(password_text.encode('utf8'), hashed)
        except ValueError:
            return False

    @staticmethod
    def hash_password(password):
        """
        method to hash password
        :param password:
        :return:
        """
        try:
            return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt(12))
        except ValueError:
            return False

    @classmethod
    def identify_handler(cls, payload) -> UserModel:
        """
        jwt method to retrieve user identity
        :param payload:
        :return:
        """
        if not isinstance(payload, str):
            users_name = payload['sub']
            user = cls.__users.find_user_by_username(users_name)
            if user:
                return user

    @classmethod
    def auth_handler(cls, username, password):
        """
        jwt method handler to verify user token
        :param username:
        :param password:
        :return:
        """
        user = cls.__users.find_user_by_username(username)
        if user and Authenticate.verify_password(password, user.user_password):
            return user
