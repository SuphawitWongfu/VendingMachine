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
    noDuplicatesProductInSameMachine = not isExistByID(MachineStock, {"product_id": query_strings["product_id"],
                                                                      "machine_id": query_strings["machine_id"]})
    productExist = isExistByID(Products, {"id": query_strings["product_id"]})
    machineExist = isExistByID(Vending_machine, {"id": query_strings["machine_id"]})
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
