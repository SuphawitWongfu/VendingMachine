from app.schema import *
from app.queryUtils import *
from flask import Blueprint, request, jsonify, redirect, url_for, flash

"""
This file contains CRUD operation regarding products table
all endpoints are redirected back to /products/ which return JSON object of the data in the products table
"""

products = Blueprint('products', __name__)

'''
this function are for validating if the query strings argument are valid or not
query_strings - the query strings which are passed in as argument in the url
return true if all criteria are passed else return false
'''


def add_validate(query_strings):
    query_strings_are_valid = are_all_query_string_present(query_strings,
                                                           ("product_name", "product_code", "product_quantity",
                                                     "price_per_unit"))
    quantity_not_negative = int(query_strings["product_quantity"]) >= 0
    price_not_negative = int(query_strings["price_per_unit"]) >= 0
    return query_strings_are_valid and quantity_not_negative and price_not_negative


# add new products to the table
@products.route("/add_products/", methods=["GET", "POST"])
def add_products():
    #  making sure that all query string needed are presented
    query_strings = request.args
    # making sure that all query string needed are presented
    addable = add_validate(query_strings)
    if not addable:
        return bad_request_400
    # noinspection PyTypeChecker
    new_vend = Products(query_strings["product_name"], query_strings["product_code"],
                        query_strings["product_quantity"], query_strings["price_per_unit"])
    add_obj_to_db(new_vend)
    return redirect(url_for("products.view_products"))


# view all products in the table
@products.route("/products/", methods=["GET"])
def view_products():
    queries = get_all_from_table(Products)
    if not queries:
        return no_content_204  # return 204 NO CONTENT if the table is empty
    prods = dict_helper(queries)
    return jsonify(prods)


# edit products in the table according to query strings given
@products.route("/edit_products/", methods=["GET", "POST"])
def edit_vending_machine():
    query_strings = request.args
    # check if the target machine exist in the database
    if query_strings and "id" in query_strings:
        update_database_row_by_id(Products, query_strings)
    return redirect(url_for("products.view_products"))


# delete a product specify by id
@products.route('/delete_products/', methods=["GET", "POST", "DELETE"])
def delete_vending_machine():
    query_strings = request.args
    provided_id = are_all_query_string_present(query_strings, ("id",))
    if not provided_id:
        return bad_request_400
    stock_obj_list = select_obj_list(MachineStock, {"product_id": query_strings["id"]})
    for obj in stock_obj_list:
        delete_obj_from_db(obj)
    unwanted_product = select_obj(Products, {"id": query_strings["id"]})
    delete_obj_from_db(unwanted_product)
    return redirect(url_for("products.view_products"))
