from flask import Flask

from .app import initialize


def create_app():

    app = Flask(__name__)

    initialize(app)

    return app