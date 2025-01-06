import subprocess
import os
import json


def get_devices():

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

        item["is_dir"] = 1 if is_dir else 0
        
        result.append(item)

    return result

    # def read_folder(path):
    #     result = {}
    #     try:
    #         with os.scandir(path) as entries:
    #             for entry in entries:
    #                 if entry.is_dir():
    #                     result[entry.name] = read_folder(entry.path)
    #                 elif entry.is_file():
    #                     result[entry.name] = None
    #     except PermissionError:
    #         result = "Access denied"
    #     return result

    # return {os.path.basename(path): read_folder(path)}
