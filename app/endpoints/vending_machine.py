from flask import Blueprint, Response, jsonify, redirect, request, url_for

from app.database.queryUtils import (
    add_obj_to_db,
    are_all_query_string_present,
    bad_request_400,
    delete_obj_from_db,
    dict_helper,
    get_all_from_table,
    no_content_204,
    select_obj,
    select_obj_list,
    update_database_row_by_id,
    update_warehouse_quantity,
)
from app.database.schema import MachineStock, vendingMachine

"""
This file contains CRUD operation regarding vending_machine table
all endpoints are redirected back to /vendings/ which return JSON object of the data in the vending_machines table
"""

vending_machine = Blueprint("vending_machine", __name__)


@vending_machine.route("/add_vendings/", methods=["POST"])
def add_vending_machine() -> Response:
    query_strings = request.args
    # making sure that all query string needed are presented
    addable = are_all_query_string_present(
        query_strings, ("machine_name", "machine_location")
    )
    if not addable:
        return bad_request_400
    new_vend = vendingMachine(
        query_strings["machine_name"], query_strings["machine_location"]
    )
    add_obj_to_db(new_vend)
    return redirect(url_for("vending_machine.view_vending_machine"))


@vending_machine.route("/vendings/", methods=["GET"])
def view_vending_machine() -> Response:
    queries = get_all_from_table(vendingMachine)
    if not queries:
        return no_content_204  # return 204 NO CONTENT if the table is empty
    vending_machines = dict_helper(queries)
    return jsonify(vending_machines)


@vending_machine.route("/edit_vendings/", methods=["POST"])
def edit_vending_machine() -> Response:
    query_strings = request.args
    # check if the target machine exist in the database
    if query_strings and "id" in query_strings:
        update_database_row_by_id(vendingMachine, query_strings)
    return redirect(url_for("vending_machine.view_vending_machine"))


@vending_machine.route("/delete_vendings/", methods=["DELETE"])
def delete_vending_machine() -> Response:
    query_strings = request.args
    provided_id = are_all_query_string_present(query_strings, ("id",))
    if not provided_id:
        return bad_request_400
    stock_obj_list = select_obj_list(MachineStock, {"machine_id": query_strings["id"]})
    for obj in stock_obj_list:
        update_warehouse_quantity(obj.product_id, obj.quantity, 0)
        delete_obj_from_db(obj)
    unwanted_vending_machine = select_obj(vendingMachine, {"id": query_strings["id"]})
    delete_obj_from_db(unwanted_vending_machine)
    return redirect(url_for("vending_machine.view_vending_machine"))
