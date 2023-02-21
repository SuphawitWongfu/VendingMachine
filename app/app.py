from flask import Flask
from flask_wtf import CSRFProtect
from flask_swagger_ui import get_swaggerui_blueprint

from app.database.db import mysql_uri, secret_key
from app.database.engine import Base, Engine
from app.endpoints.stock_timelines import stock_timelines
from app.endpoints.machine_stocks import machine_stocks
from app.endpoints.products import products
from app.endpoints.vending_machine import vending_machine

"""
This file is for running the app. To run the app, type "flask run" in the terminal
"""


def create_app() -> Flask:
    app = Flask(__name__)
    csrf = CSRFProtect()
    csrf.init_app(app)

    SWAGGER_URL = "/swagger"
    API_URL = "/static/openapi.yaml"
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Vending Machine"}
    )

    # register Blueprints

    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    app.register_blueprint(vending_machine)

    app.register_blueprint(products)

    app.register_blueprint(machine_stocks)

    app.register_blueprint(stock_timelines)

    app.secret_key = secret_key

    @app.route("/", methods=["GET"])
    def index() -> str:
        return "Vending Machine"

    # setup app config
    app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.app_context().push()

    Base.metadata.create_all(Engine)

    return app
