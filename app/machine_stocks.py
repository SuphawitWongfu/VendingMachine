from app.queryUtils import *
from flask import Blueprint, request, jsonify, redirect, url_for, flash

machine_stocks = Blueprint("machine_stocks", __name__)


def add_validate(query_strings):
    QueryStringsAreValid = areAllQueryStringPresent(query_strings, ("machine_id", "product_id", "quantity"))
    # one machine cannot have the same entry of the same type of product
    noDuplicatesProductInSameMachine = not isExist(MachineStock, {"product_id": query_strings["product_id"],
                                                                  "machine_id": query_strings["machine_id"]})
    productExist = isExist(Products, {"id": query_strings["product_id"]})
    machineExist = isExist(Vending_machine, {"id": query_strings["machine_id"]})
    quantityNotNegative = int(query_strings["quantity"]) >= 0
    productEnough = False
    if productExist:
        product = selectObj(Products, {"id": query_strings["product_id"]})
        productEnough = int(product.product_quantity) >= int(query_strings["quantity"])
    return QueryStringsAreValid and noDuplicatesProductInSameMachine and productExist and machineExist and \
        quantityNotNegative and productEnough


@machine_stocks.route("/add_machine_stocks/", methods=["GET", "POST"])
def add_machine_stocks():
    query_strings = request.args
    addable = add_validate(query_strings)

    if not addable:
        return badRequest400
    new_machine_stock = MachineStock(int(query_strings["machine_id"]), int(query_strings["product_id"]),
                                     int(query_strings["quantity"]))
    addObjToDB(new_machine_stock)
    updateWarehouseQuantity(query_strings["product_id"], 0, query_strings["quantity"])

    return redirect(url_for("machine_stocks.view_machine_stocks"))


@machine_stocks.route("/machine_stocks/", methods=["GET"])
def view_machine_stocks():
    queries = getAllFromTable(MachineStock)
    noData = not queries
    if noData:
        return noContent204  # return 204 NO CONTENT if the table is empty
    stock_list = dict_helper(queries)
    return jsonify(stock_list)


@machine_stocks.route("/edit_machine_stocks/", methods=["GET", "POST"])
def edit_machine_stock():
    query_strings = request.args
    # check if the target product exist in the database
    if query_strings and "id" in query_strings and isExist(MachineStock, {"id": query_strings["id"]}):
        stock_obj = selectObj(MachineStock, {"id": query_strings["id"]})
        quantity_in_machine = stock_obj.quantity
        quantity_validation = updateWarehouseQuantity(stock_obj.product_id, quantity_in_machine,
                                                      query_strings["quantity"])
        if quantity_validation is not None:
            updateDatabaseRowByID(MachineStock, query_strings)

    return redirect(url_for("machine_stocks.view_machine_stocks"))


@machine_stocks.route("/delete_machine_stocks/", methods=["GET", "POST", "DELETE"])
def delete_machine_stock():
    query_strings = request.args
    provided_id = areAllQueryStringPresent(query_strings, ("id",))
    if not provided_id:
        return badRequest400
    if isExist(MachineStock, {"id": query_strings["id"]}):
        unwanted_product = selectObj(MachineStock, {"id": query_strings["id"]})
        updateWarehouseQuantity(unwanted_product.product_id, unwanted_product.quantity, 0)
        deleteObjFromDB(unwanted_product)
    return redirect(url_for("machine_stocks.view_machine_stocks"))


def create_listing(machine_id):
    session = Session()
    try:
        # query vending machine for id and name
        stock_obj_list = selectObjList(MachineStock, {"machine_id": machine_id})
        machine_obj = selectObj(Vending_machine, {"id": machine_id})
        stock_dict = {"machine_id": machine_obj.id, "machine_name": machine_obj.machine_name}
        product_listing = []
        # query products for product data
        for listing in stock_obj_list:
            product_obj = session.query(Products).filter_by(id=listing.product_id).first()
            product_dict = product_obj.obj_to_dict()
            # need to change this to quantity in the vending machine
            product_dict["product_quantity"] = listing.quantity
            product_listing.append(product_dict)
        session.close()
        stock_dict["products"] = product_listing
    except:
        session.close()
        return noContent204
    return stock_dict


@machine_stocks.route("/inspect_stocks/", methods=["GET"])
def inspect_stock():
    query_strings = request.args
    if query_strings and "machine_id" in query_strings:
        stock_dict = create_listing(query_strings["machine_id"])
        return jsonify(stock_dict)
    return noContent204
