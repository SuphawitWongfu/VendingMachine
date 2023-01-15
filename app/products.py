from app.schema import *
from flask import Blueprint, request, jsonify, redirect, url_for, flash

"""
This file contains CRUD operation regarding products table
all endpoints are redirected back to /products/ which return JSON object of the data in the products table
"""

products = Blueprint('products', __name__)

# add new products to the table
@products.route("/add_products/", methods=["GET", "POST"])
def add_products():
    args = request.args
    #  making sure that all query string needed are presented
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
    return redirect(url_for("products.view_products"))

# view all products in the table
@products.route("/products/", methods=["GET"])
def view_products():
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

# edit products in the table according to query strings given
@products.route("/edit_products/", methods=["GET", "POST"])
def edit_vending_machine():
    args = request.args
    # check if the target product exist in the database
    if args and "id" in args:
        session = Session()
        current_product = session.query(Products).filter_by(id=args["id"]).first()
        if "name" in args:
            current_product.product_name = args["name"]
        if "code" in args:
            current_product.product_code = args["code"]
        if "quantity" in args:
            current_product.product_quantity = args["quantity"]
        if "price" in args:
            current_product.price_per_unit = args["price"]
        try:
            session.commit()
        except:
            session.close()
        session.close()
    return redirect(url_for("products.view_products"))

# delete a product specify by id
@products.route('/delete_products/', methods=["GET", "POST", "DELETE"])
def delete_vending_machine():
    args = request.args
    if args and "id" in args:
        session = Session()
        unwanted_product = session.query(Products).filter_by(id=args["id"]).first()
        try:
            session.delete(unwanted_product)
            session.commit()
        except:
            session.close()
        session.close()
    return redirect(url_for("products.view_products"))
