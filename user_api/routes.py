"""
Urls class , to handel request urls,
"""
from user_api.views.login_view import LoginController
from user_api.views.logout_view import LogoutController
from user_api.views.signup_view import SignUpController
from user_api.views.status_view import UserStatusController


class Urls:
    """
    Class to generate urls
    """

    @staticmethod
    def generate(app):

        """Authentication routes"""
        app.add_url_rule('/api/v1/auth/signup/', view_func=SignUpController.as_view('sign_up_user'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/login/', view_func=LoginController.as_view('login_user'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/status', view_func=UserStatusController.as_view('user_status'),
                         methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/logout', view_func=LogoutController.as_view('logout'),
                         methods=['POST'], strict_slashes=False)
