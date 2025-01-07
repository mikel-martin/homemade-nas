from flask import render_template, send_from_directory, send_file, jsonify, request
from flask_cors import cross_origin

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import controllers
import utils


def initialize(app):

    @app.route("/")
    def devices():
        return render_template("devices.html", devices=controllers.get_devices())

    @cross_origin()
    @app.route("/api/devices")
    def api_devices():
        return controllers.get_devices()


    @app.route("/folder")
    def folder():
        
        path = request.args.get("path")
        
        if not path:
            return render_template("error.html", error_code=400, message="Path not provided")
        
        if not os.path.exists(path):
            return render_template("error.html", error_code=404, message="Path not found")
        
        folder = controllers.get_folder(path)
        
        return render_template("folder.html", folder=folder, current_path=path, allowed_extensions=utils.allowed_extensions())
    

    @cross_origin()
    @app.route("/api/folder")
    def api_folder():

        path = request.args.get("path")
        
        if not path:
            return "Path not provided", 400
        
        if not os.path.exists(path):
            return "Path not found", 400
        
        folder = controllers.get_folder(path)
        
        return jsonify(path=path, folder=folder)
    

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

    
    @app.route("/api/download")
    def api_download():
        
        path = request.args.get("path")

        if not path:
            return "Path not provided", 400
        
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
        

    @app.route("/upload", methods=['POST'])
    def upload():

        path = request.form.get("path")

        if not path:
            return render_template("error.html", error_code=400, message="Path not provided")
        
        if not os.path.exists(path):
            return render_template("error.html", error_code=404, message="Path not found")

        if "files" not in request.files:
            return render_template("error.html", error_code=400, message="Request has no files")
        
        files = request.files.getlist("files")

        print(files)

        if len(files) == 0:
            return render_template("error.html", error_code=400, message="No selected files")
        
        uploaded_files = []

        for file in files:
            if file and utils.allowed_file(file.filename):
                filename = os.path.join(path, file.filename)
                file.save(filename)
                uploaded_files.append(filename)

        return jsonify(uploaded_files)
    

    @cross_origin()
    @app.route("/api/upload", methods=['POST'])
    def api_upload():

        path = request.form.get("path")

        if not path:
            return "Path not provided", 400
        
        if not os.path.exists(path):
            return "Path not found", 400

        if "files" not in request.files:
            return "Request has no files", 400
        
        files = request.files.getlist("files")

        print(files)

        if len(files) == 0:
            return "No selected files", 400
        
        uploaded_files = []

        for file in files:
            if file and utils.allowed_file(file.filename):
                filename = os.path.join(path, file.filename)
                file.save(filename)
                uploaded_files.append(filename)

        return jsonify(uploaded_files)