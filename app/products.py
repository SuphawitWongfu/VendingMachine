from app.schema import *
from flask import Blueprint, request, jsonify, redirect, url_for, flash

"""
This file contains CRUD operation regarding products table
"""

products = Blueprint('products', __name__)


@products.route("/add_products/")
def add_products():
    args = request.args
    if args and all(k in args for k in ("name", "code", "quantity", "price")):
        session = Session()
        try:
            # noinspection PyTypeChecker
            new_product = Products(args["name"], args["code"], args["quantity"], args["price"])
            session.add(new_product)
            session.commit()
        except:
            session.close()
        session.close()
    return view_vending_machine()


@products.route("/products/", methods=["GET"])
def view_vending_machine():
    session = Session()
    queries = session.query(Products).all()
    session.close()
    if not queries:
        return '', 204  # return 204 NO CONTENT if the table is empty
    prods = []
    for query in queries:
        product = {'id': query.id, 'name': query.product_name, 'product code': query.product_code,
                   'price': query.price_per_unit, 'quantity': query.product_quantity}
        prods.append(product)
    return jsonify(prods)
