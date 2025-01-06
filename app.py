from flask import render_template
from flask import request

import json

from .controllers import *


def initialize(app):

    @app.route("/")
    def devices():
        return render_template("devices.html", devices=get_devices())

    @app.route("/folder")
    def folder():
        path = request.args.get("path")
        if not path:
            return "Path not provided", 400
        folder = get_folder(path)
        print(folder)
        return render_template("folder.html", folder=folder, current_path=path)
