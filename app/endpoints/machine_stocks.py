from typing import Any, Dict

from flask import Blueprint, Response, jsonify, redirect, request, url_for
from sqlalchemy.exc import SQLAlchemyError
import datetime as dt

from app.database.engine import Session
from app.database.queryUtils import (
    add_obj_to_db,
    are_all_query_string_present,
    bad_request_400,
    delete_obj_from_db,
    dict_helper,
    get_all_from_table,
    is_exist,
    no_content_204,
    select_obj,
    select_obj_list,
    update_database_row_by_id,
    update_warehouse_quantity,
)
from app.database.schema import MachineStock, Products, VendingMachine, Timeline

view_machine_stock_endpoint = "machine_stocks.view_machine_stocks"

"""
this file contains all function regarding CRUD operation for machine_stock table
"""

machine_stocks = Blueprint("machine_stocks", __name__)

"""
this function are for validating if the query strings argument are valid or not
query_strings - the query strings which are passed in as argument in the url
return true if all criteria are passed else return false
"""


def validate_product_and_machine(query_strings: Dict[str, str]) -> bool:
    query_strings_are_valid = are_all_query_string_present(
        query_strings, ("machine_id", "product_id", "quantity")
    )
    no_duplicate_product_in_the_same_machine = not is_exist(
        MachineStock,
        {
            "product_id": query_strings["product_id"],
            "machine_id": query_strings["machine_id"],
        },
    )
    product_exists = is_exist(Products, {"id": query_strings["product_id"]})
    machine_exists = is_exist(VendingMachine, {"id": query_strings["machine_id"]})
    return (
        product_exists
        and machine_exists
        and no_duplicate_product_in_the_same_machine
        and query_strings_are_valid
    )


def validate_product_quantity(
    query_strings: Dict[str, str], product_available: bool
) -> bool:
    quantity_not_negative = int(query_strings["quantity"]) >= 0
    product_is_enough = False
    if product_available:
        product = select_obj(Products, {"id": query_strings["product_id"]})
        product_is_enough = int(product.product_quantity) >= int(
            query_strings["quantity"]
        )
    return product_is_enough and quantity_not_negative


def add_validate(query_strings: Dict[str, str]) -> bool:
    product_and_machine_available = validate_product_and_machine(query_strings)
    product_quantity_is_valid = validate_product_quantity(
        query_strings, product_and_machine_available
    )
    return product_and_machine_available and product_quantity_is_valid


@machine_stocks.route("/add_machine_stocks/", methods=["POST"])
def add_machine_stocks() -> Response:
    query_strings = request.args
    addable = add_validate(query_strings)

    if not addable:
        return bad_request_400
    new_machine_stock = MachineStock(
        int(query_strings["machine_id"]),
        int(query_strings["product_id"]),
        int(query_strings["quantity"]),
    )
    add_obj_to_db(new_machine_stock)
    new_stock_timeline = Timeline(
        machine_id=int(query_strings["machine_id"]),
        product_id=int(query_strings["product_id"]),
        quantity=int(query_strings["quantity"]),
        state=jsonify(create_listing(query_strings["machine_id"])).json,
        time_line=dt.datetime.utcnow(),
    )
    add_obj_to_db(new_stock_timeline)
    update_warehouse_quantity(query_strings["product_id"], 0, query_strings["quantity"])

    return redirect(url_for(view_machine_stock_endpoint))


@machine_stocks.route("/machine_stocks/", methods=["GET"])
def view_machine_stocks() -> Response:
    queries = get_all_from_table(MachineStock)
    no_data = not queries
    if no_data:
        return no_content_204  # return 204 NO CONTENT if the table is empty
    stock_list = dict_helper(queries)
    return jsonify(stock_list)


@machine_stocks.route("/edit_machine_stocks/", methods=["POST"])
def edit_machine_stock() -> Response:
    query_strings = request.args
    # check if the target product exist in the database
    if (
        query_strings
        and "id" in query_strings
        and is_exist(MachineStock, {"id": query_strings["id"]})
    ):
        stock_obj = select_obj(MachineStock, {"id": query_strings["id"]})
        quantity_in_machine = stock_obj.quantity
        quantity_validation = update_warehouse_quantity(
            stock_obj.product_id, quantity_in_machine, query_strings["quantity"]
        )
        if quantity_validation is not None:
            update_database_row_by_id(MachineStock, query_strings)
            new_stock_timeline = Timeline(
                machine_id=int(stock_obj.machine_id),
                product_id=int(stock_obj.product_id),
                quantity=int(query_strings["quantity"]),
                state=jsonify(create_listing(stock_obj.machine_id)).json,
                time_line=dt.datetime.utcnow(),
            )
            add_obj_to_db(new_stock_timeline)

    return redirect(url_for(view_machine_stock_endpoint))


@machine_stocks.route("/delete_machine_stocks/", methods=["DELETE"])
def delete_machine_stock() -> Response:
    query_strings = request.args
    provided_id = are_all_query_string_present(query_strings, ("id",))
    if not provided_id:
        return bad_request_400
    if is_exist(MachineStock, {"id": query_strings["id"]}):
        unwanted_product = select_obj(MachineStock, {"id": query_strings["id"]})
        update_warehouse_quantity(
            unwanted_product.product_id, unwanted_product.quantity, 0
        )
        delete_obj_from_db(unwanted_product)
        new_stock_timeline = Timeline(
            machine_id=int(unwanted_product.machine_id),
            product_id=int(unwanted_product.product_id),
            quantity=0,
            state=jsonify(create_listing(str(unwanted_product.machine_id))).json,
            time_line=dt.datetime.utcnow(),
        )
        add_obj_to_db(new_stock_timeline)

    return redirect(url_for(view_machine_stock_endpoint), code=303)


"""
this function create a dictionary of listings of items in a specify vending_machine
machine_id - the id of the vending_machine we wish to see the listings
return a dictionary of listings
"""


def create_listing(machine_id: str) -> dict[str, str | int | list[Any]] | Any:
    session = Session()
    try:
        # query vending machine for id and name
        stock_obj_list = select_obj_list(MachineStock, {"machine_id": machine_id})
        machine_obj = select_obj(VendingMachine, {"id": machine_id})
        stock_dict = {
            "machine_id": machine_obj.id,
            "machine_name": machine_obj.machine_name,
        }
        product_listing = []
        # query products for product data
        for listing in stock_obj_list:
            product_obj = (
                session.query(Products).filter_by(id=listing.product_id).first()
            )
            product_dict = product_obj.obj_to_dict()
            # need to change this to quantity in the vending machine
            product_dict["product_quantity"] = listing.quantity
            product_listing.append(product_dict)
        session.close()
        stock_dict["products"] = product_listing
    except SQLAlchemyError:
        session.close()
        return no_content_204
    return stock_dict


# display the listings of a vending machine which id is specified in query strings
@machine_stocks.route("/inspect_stocks/", methods=["GET"])
def inspect_stock() -> Response:
    query_strings = request.args
    if query_strings and "machine_id" in query_strings:
        stock_dict = create_listing(query_strings["machine_id"])
        return jsonify(stock_dict)
    return no_content_204
