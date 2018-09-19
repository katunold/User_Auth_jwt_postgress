"""
Module to handle user logout
"""
from flask import request, make_response, jsonify
from flask.views import MethodView

from user_api.auth.user_auth import Authenticate
from user_api.models.token_model import Tokens


class LogoutController(MethodView):
    """
    Logout resource
    """
    def post(self):
        # get auth_token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(' ')[1]
        else:
            auth_token = ''

        if auth_token:
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
                # mark the token as blacklisted
                blacklist_token = Tokens().blacklist_token(auth_token)

                if blacklist_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged out.',
                        'token_blacklisted': blacklist_token.token
                    }
                    return make_response(jsonify(response_object)), 200
                response_object = {
                    'status': 'fail',
                    'message': 'Error occurred'
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
            return make_response(jsonify(response_object)), 403
