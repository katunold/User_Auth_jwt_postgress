"""
Module for the user resource
"""
import copy

from flask import request, make_response, jsonify
from flask.views import MethodView

from user_api.auth.user_auth import Authenticate
from user_api.models.token_model import Tokens
from user_api.models.user_model import Users


class UserStatusController(MethodView):
    """
    User resource
    """
    all_users = Users()

    def get(self):

        # get the auth_token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response_object = {
                    'status': 'fail',
                    'message': 'Bearer token malformed'
                }
                return make_response(jsonify(response_object)), 401
        else:
            auth_token = ' '

        if auth_token:
            resp = Authenticate.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = self.all_users.find_user_by_id(resp)
                user = copy.deepcopy(user)
                del user.user_password
                response_object = {
                    'status': 'success',
                    'data': user.__dict__
                }
                return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object)), 401
