from flask import render_template

from .controllers import get_devices


def initialize_routes(app):
    
    # Get list of all mounted devices
    @app.route("/")
    def devices():
        return render_template("devices.html", devices=get_devices())