import datetime
import time
from unittest import TestCase

from flask import json

from user_api.config.config import TestingConfig
from user_api.config.database import DatabaseConnection
from user_api.models.token_model import Tokens
from run import APP


class TestUserAuth(TestCase):
    def setUp(self):
        APP.config.from_object(TestingConfig)
        self.client = APP.test_client
        self.database = DatabaseConnection()
        self.database.init_db(APP)
        self.token = None

    def tearDown(self):
        self.database.drop_test_schema()

    def register_user(self, user_name=None, email=None, password=None):
        return self.client().post(
            '/api/v1/auth/signup/',
            data=json.dumps(dict(
                user_name=user_name,
                email=email,
                password=password,
                registered_on=datetime.datetime.now()
            )),
            content_type="application/json"
        )

    def test_fine_user_registration(self):
        """
        Test for user registration
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail.com', 'qwerty')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'] == 'success')
        self.assertTrue(received_data['message'] == 'Successfully registered')
        self.assertTrue(register.content_type == 'application/json')
        self.assertEqual(register.status_code, 201)

    def test_missing_fields_during_signup(self):
        """
        Test for missing fields during user registration
        :return:
        """
        register = self.client().post(
            '/api/v1/auth/signup/',
            data=json.dumps(dict(
                user_name='Arnold',
                email='arnold@gmail.com',
                registered_on=datetime.datetime.now()
            )),
            content_type="application/json"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "some of these fields are missing")
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_empty_fields_during_signup(self):
        """
        Test for empty fields during user registration
        :return:
        """
        register = self.register_user(
            "",
            "arnold@gmail.com",
            "qwerty"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "some of these fields have empty/no values")
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_invalid_email_registration(self):
        """
        Test for registration with invalid email
        :return:
        """
        register = self.register_user(
            "Arnold",
            "arnold@gmail",
            "qwerty"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'])
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_invalid_password_length(self):
        """
        Test for password less than 6 characters
        :return:
        """
        register = self.register_user(
            "Arnold",
            "arnold94@gmail",
            "qwert"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] ==
                        "Password is wrong. It should be at-least 6 characters long, and alphanumeric.")
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_for_valid_user_name(self):
        """
        Test for valid user name
        :return:
        """
        register = self.register_user(
            "12345",
            "arnold@gmail.com",
            "qwerty"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "User name cannot be only numbers")
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_for_integer_user_name(self):
        """
        Test for integers used as user name
        :return:
        """
        register = self.register_user(
            12325363,
            "arnold@gmail.com",
            "qwerty"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "Only string data type supported")
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_registration_with_existing_email(self):
        """
        Test for registration with an existing email
        :return:
        """
        self.register_user(
            "Arnold",
            "arnold@gmail.com",
            "qwerty"
        )
        register = self.register_user(
            "Arnold",
            "arnold@gmail.com",
            "qwerty"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "email is already taken.")
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 409)

    def test_registration_with_existing_user_name(self):
        """
        Test for registration with an existing user name
        :return:
        """
        self.register_user(
            "Arnold ",
            "arnold94@gmail.com",
            "qwerty"
        )
        register = self.register_user(
            "Arnold",
            "arnold@gmail.com",
            "qwerty"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "Username already taken.")
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 409)

    def test_for_registered_user_login(self):
        """
        Test for proper registered user login
        :return:
        """
        self.register_user(
            "Arnold",
            "arnold94@gmail.com",
            "qwerty"
        )
        login_user = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name="Arnold",
                password="qwerty",
            )),
            content_type='application/json'
        )

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'] == 'success')
        self.assertTrue(response_data['message'] == 'Welcome, You are now logged in')
        self.assertTrue(response_data['auth_token'])
        self.assertTrue(login_user.content_type == 'application/json')
        self.assertEqual(login_user.status_code, 200)

    def test_non_registered_user_login(self):
        """
        Test for login of a non registered user
        :return:
        """
        login_user = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name="Arnold",
                password="qwerty",
            )),
            content_type='application/json'
        )
        data = json.loads(login_user.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'User does not exist.')
        self.assertTrue(login_user.content_type == 'application/json')
        self.assertEqual(login_user.status_code, 404)

    def test_correct_email_wrong_password(self):
        """
        Test for login with correct email and wrong password
        :return:
        """
        # register the user

        self.register_user(
            "Arnold",
            "arnold@gmail.com",
            "qwerty"
        )

        # login the registered user with a wrong password
        login_user = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name="Arnold",
                password="qwertyuiop",
            )),
            content_type='application/json'
        )
        data = json.loads(login_user.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'User does not exist.')
        self.assertTrue(login_user.content_type == 'application/json')
        self.assertEqual(login_user.status_code, 404)

    def test_user_status(self):
        """
        Tests for thee user status
        :return:
        """
        self.register_user(
            "Arnold",
            "arnold@gmail.com",
            "qwerty"
        )

        login_user = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name="Arnold",
                password="qwerty",
            )),
            content_type='application/json'
        )

        response = self.client().get(
            '/api/v1/auth/status',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    login_user.data.decode()
                )['auth_token']
            )
        )

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['data'] is not None)
        self.assertTrue(data['data']['user_email'] == 'arnold@gmail.com')
        self.assertTrue(data['data']['user_name'] == 'Arnold')
        self.assertEqual(response.status_code, 200)

    def test_valid_logout(self):
        """ Test for logout before token expires """

        # user registration
        self.register_user(
            "Arnold",
            "arnold@gmail.com",
            "qwerty"
        )
        # user login
        login_user = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name="Arnold",
                password="qwerty",
            )),
            content_type='application/json'
        )
        # valid token logout
        response = self.client().post(
            '/api/v1/auth/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    login_user.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged out.')
        self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        """ Testing logout after the token expires """

        # user registration
        self.register_user(
            "Arnold",
            "arnold@gmail.com",
            "qwerty"
        )
        # user login
        login_user = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name="Arnold",
                password="qwerty",
            )),
            content_type='application/json'
        )

        # invalid token logout
        time.sleep(6)
        response = self.client().post(
            '/api/v1/auth/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    login_user.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'Signature expired. Please log in again.')
        self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_logout(self):
        """
        Test for logout after a valid token gets blacklisted
        :return:
        """
        # user registration
        self.register_user(
            "Arnold",
            "arnold@gmail.com",
            "qwerty"
        )

        # user login
        login_user = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name="Arnold",
                password="qwerty",
            )),
            content_type='application/json'
        )

        # blacklist a valid token
        Tokens().blacklist_token(token=json.loads(login_user.data.decode())['auth_token'])

        # blacklisted valid token logout
        response = self.client().post(
            '/api/v1/auth/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    login_user.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
        self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_user(self):
        """
        Test for user status with a blacklisted valid token
        :return:
        """
        # user registration
        self.register_user(
            "Arnold",
            "arnold@gmail.com",
            "qwerty"
        )

        # user login
        login_user = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name="Arnold",
                password="qwerty",
            )),
            content_type='application/json'
        )

        # blacklist a valid token
        Tokens().blacklist_token(token=json.loads(login_user.data.decode())['auth_token'])
        response = self.client().get(
            '/api/v1/auth/status',
            headers=dict(
                Authorization='Bearer ' + json.loads(login_user.data.decode())['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
        self.assertEqual(response.status_code, 401)

    def test_user_status_malformed_bearer_token(self):
        """
        Test for user status with malformed bearer token
        :return:
        """
        # user registration
        self.register_user(
            "Arnold",
            "arnold@gmail.com",
            "qwerty"
        )

        # user login
        login_user = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name="Arnold",
                password="qwerty",
            )),
            content_type='application/json'
        )

        response = self.client().get(
            '/api/v1/auth/status',
            headers=dict(
                Authorization='Bearer' + json.loads(login_user.data.decode())['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Bearer token malformed')
        self.assertEqual(response.status_code, 401)

