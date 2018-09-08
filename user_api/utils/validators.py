"""
Module defines validation rules used by the api
"""
import re


class Validators:
    """
    Class defines validator functions
    """

    @staticmethod
    def validate_email(email) -> bool:
        """
        Validate email address
        :param email:
        :return:
        """
        pattern = re.compile(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$")
        if not pattern.match(email):
            return False
        return True

    @staticmethod
    def validate_password(password, length) -> bool:
        """
        password validator
        :param password:
        :param length:
        :return:
        """
        if not isinstance(length, int):
            raise ValueError("length must be an integer")
        if length > len(password):
            return False
        return password.isalnum()

    @staticmethod
    def validate_username(username) -> bool:
        """
        Username validator
        :param username:
        :return:
        """
        try:
            int(username)
            return False
        except ValueError:
            return True



