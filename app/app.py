from flask import Flask, Response

from app.database.db import mysql_uri
from app.database.engine import Base, Engine
from app.endpoints.machine_stocks import machine_stocks
from app.endpoints.products import products
from app.endpoints.vending_machine import vending_machine

"""
This file is for running the app. To run the app, type "flask run" in the terminal
"""

app = Flask(__name__)

# register Blueprints

app.register_blueprint(vending_machine)

app.register_blueprint(products)

app.register_blueprint(machine_stocks)

app.config["SECRET_KEY"] = "thisisasecret"


@app.route("/", methods=["GET"])
def index() -> Response:
    return "Vending Machine"


# setup app config
app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.app_context().push()

Base.metadata.create_all(Engine)
