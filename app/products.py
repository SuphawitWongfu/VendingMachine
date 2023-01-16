from app.schema import *
from app.queryUtils import *
from flask import Blueprint, request, jsonify, redirect, url_for, flash

"""
This file contains CRUD operation regarding products table
all endpoints are redirected back to /products/ which return JSON object of the data in the products table
"""

products = Blueprint('products', __name__)


# add new products to the table
@products.route("/add_products/", methods=["GET", "POST"])
def add_products():
    #  making sure that all query string needed are presented
    query_strings = request.args
    # making sure that all query string needed are presented
    addable = areAllQueryStringPresent(query_strings,
                                       ("product_name", "product_code", "product_quantity", "price_per_unit"))
    if addable:
        # noinspection PyTypeChecker
        new_vend = Products(query_strings["product_name"], query_strings["product_code"],
                            query_strings["product_quantity"], query_strings["price_per_unit"])
        addObjToDB(new_vend)
    return redirect(url_for("products.view_products"))


# view all products in the table
@products.route("/products/", methods=["GET"])
def view_products():
    queries = getAllFromTable(Products)
    if queries is None:
        return noContent204  # return 204 NO CONTENT if the table is empty
    prods = dict_helper(queries)
    return jsonify(prods)


# edit products in the table according to query strings given
@products.route("/edit_products/", methods=["GET", "POST"])
def edit_vending_machine():
    query_strings = request.args
    # check if the target machine exist in the database
    if query_strings and "id" in query_strings:
        updateDatabaseRowByID(Products, query_strings)
    return redirect(url_for("products.view_products"))


# delete a product specify by id
@products.route('/delete_products/', methods=["GET", "POST", "DELETE"])
def delete_vending_machine():
    query_strings = request.args
    if query_strings and "id" in query_strings:
        stock_obj_list = selectObjList(MachineStock, {"product_id": query_strings["id"]})
        for obj in stock_obj_list:
            deleteObjFromDB(obj)
        unwanted_product = selectObj(Products, {"id": query_strings["id"]})
        deleteObjFromDB(unwanted_product)
    return redirect(url_for("products.view_products"))
