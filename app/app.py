from flask import Flask
from app.db import mysql_uri
from app.schema import *

"""
This file is for running the app. To run the app, type "flask run" in the terminal
"""

app = Flask(__name__)

# register Blueprints
from app.vending_machine import vending_machine

app.register_blueprint(vending_machine)
from app.products import products

app.register_blueprint(products)
from app.machine_stocks import machine_stocks

app.register_blueprint(machine_stocks)

app.config['SECRET_KEY'] = 'thisisasecret'


@app.route("/", methods=["GET"])
def index():
    return "Venting Machine"


# setup app config
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

Base.metadata.create_all(Engine)
