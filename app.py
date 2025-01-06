from flask import render_template, send_from_directory
from flask import request

import json

import os

from .controllers import *


def initialize(app):

    @app.route("/")
    def devices():
        return render_template("devices.html", devices=get_devices())


    @app.route("/folder")
    def folder():
        
        path = request.args.get("path")
        
        if not path:
            return render_template("error.html", error_code=400, message="Path not provided")
        
        if not os.path.exists(path):
            return render_template("error.html", error_code=404, message="Path not found")
        
        folder = get_folder(path)
        
        return render_template("folder.html", folder=folder, current_path=path)
    

    @app.route("/download")
    def download():
        
        path = request.args.get("path")

        if not path:
            return render_template("error.html", error_code=400, message="Path not provided")
        
        if not os.path.exists(path):
            return render_template("error.html", error_code=404, message="Path not found")
        
        return send_from_directory(os.path.dirname(path), os.path.basename(path), as_attachment=True)

