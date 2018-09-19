"""
Module for token model
"""
import datetime

from user_api.config.database import DatabaseConnection
from user_api.utils.singleton import Singleton
from user_api.utils.utils import JSONSerializable


class TokenModel(JSONSerializable):
    """
    Model to hold blacklisted tokens
    """

    def __init__(self, token=None):
        self.blacklisted_on = None
        self.token = token


class Tokens(metaclass=Singleton):
    """
    Define token module attributes accessed by callers
    """
    __table = "blacklist_token"
    __database = DatabaseConnection()

    def blacklist_token(self, token=None):

        token_blacklisted = TokenModel(token)
        token_blacklisted.blacklisted_on = datetime.datetime.now()

        data = {
            'token': token_blacklisted.token,
            'blacklisted_on': token_blacklisted.blacklisted_on
        }
        submit = self.__database.insert(self.__table, data)

        if not submit:
            return None
        return token_blacklisted

    def check_blacklist(self, auth_token):
        # check whether auth_token has been blacklisted
        criteria = {
            "token": auth_token
        }

        resp = self.__database.find(self.__table, criteria=criteria)

        if resp:
            return True
        else:
            return False
