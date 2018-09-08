import datetime

from user_api.config.database import DatabaseConnection
from user_api.utils.singleton import Singleton
from user_api.utils.utils import JSONSerializable


class UserModel(JSONSerializable):
    """
    Model to hold user data
    """
    def __init__(self, user_name=None, user_email=None, user_password=None):
        """
        User model template
        :param user_name:
        :param user_email:
        :param user_password:
        """
        self.registered_on = datetime.datetime.now()

        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password


class Users(metaclass=Singleton):
    """
    Define user module attributes accessed by callers
    """
    __table = "user"
    __database = DatabaseConnection()

    def register_user(self, user_name=None, user_email=None,
                      user_password=None) -> UserModel or None:
        """
        Register new user
        :param user_name:
        :param user_email:
        :param user_password:
        :return:
        """
        user = UserModel(user_name, user_email, user_password)

        data = {
            "user_name": user_name,
            "email": user_email,
            "registered_on": user.registered_on,
            "password": user_password.decode("utf8")
        }
        submit = self.__database.insert(self.__table, data)

        if not submit:
            return None
        return user

    def find_user_by_id(self, user_id) -> UserModel or bool:
        """
        find a specific user given an id
        :param user_id:
        :return:
        """
        criteria = {
            "user_id": user_id
        }
        res = self.__database.find(self.__table, criteria=criteria)
        if res and isinstance(res, dict):
            user = UserModel(res['user_name'], res['user_email'], None)
            user.user_id = res["user_id"]
            user.user_password = res["user_password"].encode("utf8")
            return user
        return False

    def find_user_by_username(self, username) -> UserModel or None:
        """
        find a specific user given a user name
        :return:
        :param username:
        :return:
        """
        criteria = {'user_name': username}
        res = self.__database.find(self.__table, criteria=criteria)
        if res and isinstance(res, dict):
            user = UserModel(res['user_name'], res['email'], None)
            user.user_id = res["user_id"]
            user.user_password = res["password"].encode("utf8")
            return user
        return None

    def find_user_by_email(self, email) -> UserModel or None:
        """
        find a specific user given an email
        :param email:
        :return:
        """
        criteria = {'email': email}
        res = self.__database.find(self.__table, criteria=criteria)
        if res and isinstance(res, dict):
            user = UserModel(res['user_name'], res['email'], None)
            user.user_id = res['user_id']
            user.user_password = res['password'].encode('utf8')
            return user
        return None
