from app.schema import *
from app.queryUtils import *
from flask import Blueprint, request, jsonify, redirect, url_for, flash

machine_stocks = Blueprint("machine_stocks", __name__)


def addProductToMachine(query_strings):
    session = Session()
    try:
        new_machine_stock = MachineStock(query_strings["machine_id"], query_strings["product_id"],
                                         query_strings["quantity"])
        session.add(new_machine_stock)
        # deduct quantity from the products warehouse
        product = session.query(Products).filter_by(id=query_strings["product_id"]).first()
        if product.product_quantity >= int(query_strings["quantity"]):
            product.product_quantity -= int(query_strings["quantity"])
            session.commit()
        session.close()
    except:
        session.close()


def check_item_adding_validity(query_strings):
    QueryStringsAreValid = areAllQueryStringPresent(query_strings, ("machine_id", "product_id", "quantity"))
    # one machine cannot have the same entry of the same type of product
    noDuplicatesProductInSameMachine = not isExist(MachineStock, {"product_id": query_strings["product_id"],
                                                                      "machine_id": query_strings["machine_id"]})
    productExist = isExist(Products, {"id": query_strings["product_id"]})
    machineExist = isExist(Vending_machine, {"id": query_strings["machine_id"]})
    return QueryStringsAreValid and noDuplicatesProductInSameMachine and productExist and machineExist





@machine_stocks.route("/add_machine_stocks/", methods=["GET", "POST"])
def add_machine_stocks():
    query_strings = request.args
    addable = check_item_adding_validity(query_strings)

    if addable:
        addProductToMachine(query_strings)

    return redirect(url_for("machine_stocks.view_machine_stocks"))


@machine_stocks.route("/machine_stocks/", methods=["GET"])
def view_machine_stocks():
    queries = getAllFromTable(MachineStock)
    noData = not queries
    if noData:
        noContent204 = '', 204
        return noContent204  # return 204 NO CONTENT if the table is empty
    stock_list = dict_helper(queries)
    return jsonify(stock_list)


@machine_stocks.route("/edit_machine_stocks/", methods=["GET", "POST"])
def edit_vending_machine():
    query_strings = request.args
    # check if the target product exist in the database
    if query_strings and "id" in query_strings:
        updateDatabaseRowByID(MachineStock, query_strings)

    return redirect(url_for("machine_stocks.view_machine_stocks"))

@machine_stocks.route("/delete_machine_stocks/", methods=["GET", "POST", "DELETE"])
def delete_vending_machine():
    query_strings = request.args
    if query_strings and "id" in query_strings:
        session = Session()
        unwanted_product = session.query(MachineStock).filter_by(id=query_strings["id"]).first()
        try:
            session.delete(unwanted_product)
            session.commit()
            session.close()
        except:
            session.close()
    return redirect(url_for("machine_stocks.view_machine_stocks"))


@machine_stocks.route("/inspect_stocks/", methods=["GET"])
def inspect_stock():
    query_strings = request.args
    noContent204 = '', 204
    if query_strings and "machine_id" in query_strings:
        session = Session()
        machine_obj_list = session.query(MachineStock).filter_by(machine_id=query_strings["machine_id"]).all()
        stock_listing = []
        for listing in machine_obj_list:
            product_obj = session.query(Products).filter_by(id=listing.product_id).first()
            product_dict = product_obj.obj_to_dict()
            product_dict["product_quantity"] = listing.quantity
            stock_listing.append(product_dict)
        session.close()
        return jsonify(stock_listing)
    return noContent204
