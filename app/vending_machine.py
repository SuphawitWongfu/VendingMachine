import json
from flask import Blueprint,request

vending_machine = Blueprint('vending_machine', __name__)


@vending_machine.route("/vendings/", methods=["GET", "POST"])
def add_vending_machine():
    args = request.args
    return json.dump(args)
