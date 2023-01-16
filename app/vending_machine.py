from app.queryUtils import *
from flask import Blueprint, request, jsonify, redirect, url_for, flash

"""
This file contains CRUD operation regarding vending_machine table
all endpoints are redirected back to /vendings/ which return JSON object of the data in the vending_machines table
"""

vending_machine = Blueprint('vending_machine', __name__)


# add new machine to vending machine table
@vending_machine.route("/add_vendings/", methods=["GET", "POST"])
def add_vending_machine():
    query_strings = request.args
    # making sure that all query string needed are presented
    addable = areAllQueryStringPresent(query_strings, ("machine_name", "machine_location"))
    if addable:
        # noinspection PyTypeChecker
        new_vend = Vending_machine(query_strings["machine_name"], query_strings["machine_location"])
        addObjToDB(new_vend)
    return redirect(url_for("vending_machine.view_vending_machine"))


# view all vending machines in the table
@vending_machine.route("/vendings/", methods=["GET"])
def view_vending_machine():
    queries = getAllFromTable(Vending_machine)
    if queries is None:
        return noContent204  # return 204 NO CONTENT if the table is empty
    vending_machines = dict_helper(queries)
    return jsonify(vending_machines)


# edit an instance of vending machine
@vending_machine.route("/edit_vendings/", methods=["GET", "POST"])
def edit_vending_machine():
    query_strings = request.args
    # check if the target machine exist in the database
    if query_strings and "id" in query_strings:
        updateDatabaseRowByID(Vending_machine, query_strings)
    return redirect(url_for("vending_machine.view_vending_machine"))


# delete a vending machine from the table
@vending_machine.route('/delete_vendings/', methods=["GET", "POST", "DELETE"])
def delete_vending_machine():
    query_strings = request.args
    if query_strings and "id" in query_strings:
        stock_obj_list = selectObjList(MachineStock, {"machine_id": query_strings["id"]})
        for obj in stock_obj_list:
            updateWarehouseQuantity(obj.product_id, obj.quantity, 0)
            deleteObjFromDB(obj)
        unwanted_vending_machine = selectObj(Vending_machine, {"id": query_strings["id"]})
        deleteObjFromDB(unwanted_vending_machine)
    return redirect(url_for("vending_machine.view_vending_machine"))
