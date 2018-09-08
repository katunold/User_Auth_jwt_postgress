"""
Urls class , to handel request urls,
"""
from user_api.views.signup_view import SignUpController


class Urls:
    """
    Class to generate urls
    """

    @staticmethod
    def generate(app):

        """Authentication routes"""
        app.add_url_rule('/api/v1/auth/signup/', view_func=SignUpController.as_view('sign_up_user'),
                         methods=['POST'], strict_slashes=False)
