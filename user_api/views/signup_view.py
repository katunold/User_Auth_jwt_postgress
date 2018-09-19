import copy

from flask import request, jsonify
from flask.views import MethodView

from user_api.auth.user_auth import Authenticate
from user_api.errors.return_errors import ReturnError
from user_api.models.user_model import Users
from user_api.utils.validators import Validators


class SignUpController(MethodView):
    """
    User Registration
    """
    __user = Users()

    def post(self):
        # get post data
        post_data = request.get_json()

        keys = ("user_name", "email", 'password')
        if not set(keys).issubset(set(post_data)):
            return ReturnError.missing_fields(keys)

        try:
            user_name = post_data.get("user_name").strip()
            email = post_data.get("email").strip()
            password = post_data.get("password").strip()
        except AttributeError:
            return ReturnError.invalid_data_type()

        if not user_name or not email or not password:
            return ReturnError.empty_fields()

        if not Validators.validate_password(password, 6):
            return ReturnError.invalid_password()

        if not Validators.validate_email(email):
            return ReturnError.invalid_email()

        if not Validators.validate_username(user_name):
            return ReturnError.invalid_username()

        # check if user already exists
        user_name_ = self.__user.find_user_by_username(user_name)
        user_ = self.__user.find_user_by_email(email)
        if not user_ and not user_name_:
            try:
                user = self.__user.register_user(user_name, email, Authenticate.hash_password(password))

                user = copy.deepcopy(user)
                del user.user_password

                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered'
                }
                return jsonify(response_object), 201
            except Exception as ex:
                print(ex)
                return ReturnError.error_occurred()
        elif user_:
            return ReturnError.email_already_exists()
        elif user_name_:
            return ReturnError.username_already_exists()
        else:
            return ReturnError.could_not_process_request()
