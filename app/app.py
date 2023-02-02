from flask import Flask, Response

from app.database.db import mysql_uri, secret_key
from app.database.engine import Base, Engine
from app.endpoints.machine_stocks import machine_stocks
from app.endpoints.products import products
from app.endpoints.vending_machine import vending_machine
from flask_wtf import CSRFProtect

"""
This file is for running the app. To run the app, type "flask run" in the terminal
"""


def create_app() -> Flask:
    app = Flask(__name__)
    csrf = CSRFProtect()
    csrf.init_app(app)

    # register Blueprints

    app.register_blueprint(vending_machine)

    app.register_blueprint(products)

    app.register_blueprint(machine_stocks)

    app.secret_key = secret_key

    @app.route("/", methods=["GET"])
    def index() -> Response:
        return "Vending Machine"

    # setup app config
    app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.app_context().push()

    Base.metadata.create_all(Engine)

    return app
