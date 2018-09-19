"""
Main app root of the api endpoints
"""
from flask import Flask

from user_api.config.config import HostConfig, DevelopmentConfig
from user_api.config.database import DatabaseConnection
from user_api.routes import Urls


class Server:
    """
    Creates the flask object to start the server
    """

    @staticmethod
    def create_app(env=None):
        app = Flask(__name__)
        app.config.update(env.__dict__ or {})
        Urls.generate(app)

        with app.app_context():
            database = DatabaseConnection()
            database.init_db(app)
        return app


APP = Server().create_app(env=DevelopmentConfig)

if __name__ == '__main__':
    APP.run(host=HostConfig.HOST, port=HostConfig.PORT)
