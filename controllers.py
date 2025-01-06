from flask import render_template, send_from_directory
import subprocess
import os

import utils


def get_devices():

    utils.allowed_extensions()

    result = subprocess.run("df -h | grep -v none | grep ^/dev", shell=True, text=True, capture_output=True, check=True)

    devices = []

    for line in result.stdout.strip().split("\n"):
        columns = line.split()
        if len(columns) >= 6:
            devices.append({
                "file_system": columns[0],
                "size": columns[1],
                "used": columns[2],
                "avail": columns[3],
                "use_per": columns[4],
                "mounted_on": columns[5],
            })

    return devices


def get_folder(path):

    result = []

    for entry in os.listdir(path):
        
        item = {}

        abs_path = os.path.join(path, entry)
        rel_path = os.path.relpath(abs_path, start=path)

        is_dir = os.path.isdir(abs_path)

        item["abs"] = abs_path
        item["rel"] = rel_path

        item["size"] = utils.get_file_size(abs_path) if not is_dir else "-"

        item["is_dir"] = 1 if is_dir else 0
        
        result.append(item)

    return result

def download(abs_path):

    if not abs_path:
        return render_template("error.html", error_code=400, message="Path not provided")

    if not os.path.exists(abs_path):
        return render_template("error.html", error_code=400, message="File not found")

    return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path), as_attachment=True)
