from flask import render_template, send_from_directory, send_file
from flask import request

import os
import sys
import zipfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import controllers
import utils


def initialize(app):

    @app.route("/")
    def devices():
        return render_template("devices.html", devices=controllers.get_devices())


    @app.route("/folder")
    def folder():
        
        path = request.args.get("path")
        
        if not path:
            return render_template("error.html", error_code=400, message="Path not provided")
        
        if not os.path.exists(path):
            return render_template("error.html", error_code=404, message="Path not found")
        
        folder = controllers.get_folder(path)
        
        return render_template("folder.html", folder=folder, current_path=path)
    

    @app.route("/download")
    def download():
        
        path = request.args.get("path")

        if not path:
            return render_template("error.html", error_code=400, message="Path not provided")
        
        if not os.path.exists(path):
            return render_template("error.html", error_code=404, message="Path not found")
        
        if os.path.isdir(path):

            zip_path = f"/tmp/{os.path.basename(path)}.zip"

            utils.zip_folder(path, zip_path)

            try:
                return send_file(zip_path, as_attachment=True, download_name=f"{os.path.basename(path)}.zip")
            finally:
                if os.path.exists(zip_path):
                    os.remove(zip_path)

        else:
            return send_from_directory(os.path.dirname(path), os.path.basename(path), as_attachment=True)
        
    

    @app.route("/download-folder")
    def download_folder():
        
        path = request.args.get("path")

        if not path:
            return render_template("error.html", error_code=400, message="Path not provided")
        
        if not os.path.exists(path):
            return render_template("error.html", error_code=404, message="Path not found")
        
        if not os.path.isdir(path):
            return render_template("error.html", error_code=404, message="Path is not a folder")
        
        zip_path = f"/tmp/{os.path.basename(path)}.zip"

        utils.zip_folder(path, zip_path)

        try:
            return send_file(zip_path, as_attachment=True, download_name=f"{os.path.basename(path)}.zip")
        finally:
            if os.path.exists(zip_path):
                os.remove(zip_path)
