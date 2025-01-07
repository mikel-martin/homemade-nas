from flask_cors import CORS
from flask import Flask

from .app import initialize


def create_app():

    app = Flask(__name__)

    cors = CORS(app)

    app.config["CORS_HEADERS"] = "Content-Type"

    initialize(app)

    return app