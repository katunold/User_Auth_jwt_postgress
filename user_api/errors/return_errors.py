from flask import jsonify, request


class ReturnError:

    @staticmethod
    def missing_fields(keys):
        return jsonify({"status": "fail",
                        "error_message": "some of these fields are missing",
                        "data": keys}), 400

    @staticmethod
    def empty_fields():
        return jsonify({"status": "fail",
                        "error_message": "some of these fields have empty/no values",
                        "data": request.get_json()}), 400

    @staticmethod
    def invalid_password():
        return jsonify({
            "status": "fail",
            "error_message": "Password is wrong. It should be at-least 6 characters"
                             " long, and alphanumeric.", "data": request.get_json()}), 400

    @staticmethod
    def invalid_username():
        return jsonify({
            "status": "fail",
            "error_message": "User name cannot be only numbers",
            "data": request.get_json()}), 400

    @staticmethod
    def invalid_email():
        req = request.get_json()
        return jsonify({
            "status": "fail",
            "error_message": "User email {0} is wrong, It should be "
                             "in the format (xxxxx@xxxx.xxx)".format(req['email']),
            "data": req
        }), 400

    @staticmethod
    def error_occurred():
        response_object = {
            'data': False,
            'error_message': 'Sorry please try again'
        }
        return jsonify(response_object), 400

    @staticmethod
    def email_already_exists():
        response_object = {
            'status': 'fail',
            'data': False,
            'error_message': 'email is already taken.',
        }
        return jsonify(response_object), 409

    @staticmethod
    def username_already_exists():
        response_object = {
            'status': 'fail',
            'data': False,
            'error_message': 'Username already taken.',
        }
        return jsonify(response_object), 409

    @staticmethod
    def could_not_process_request():
        return jsonify({"error_message": "Request could not be processed.",
                        "data": False}), 400

    @staticmethod
    def invalid_data_type():
        return jsonify({
            "status": "fail",
            "error_message": "Only string data type supported",
            "data": False}), 400
