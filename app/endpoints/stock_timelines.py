from flask import Blueprint, request, jsonify, Response

from app.database.queryUtils import select_obj_list
from app.database.schema import Timeline
from app.database.queryUtils import no_content_204

stock_timelines = Blueprint("stock_timelines", __name__)


@stock_timelines.route("/get_product_timestamps/", methods=["GET"])
def get_product_timestamps() -> Response:
    query_strings = request.args
    machine_id = query_strings["machine_id"]
    results = select_obj_list(Timeline, {"machine_id": machine_id})
    if len(results) == 0:
        return no_content_204
    products = []
    for result in results:
        result.state["date"] = result.time_line
        products.append(result.state)
    return jsonify(products)


@stock_timelines.route("/get_quantity_timestamps/", methods=["GET"])
def get_quantity_timestamps() -> Response:
    query_strings = request.args
    product_id = query_strings["product_id"]
    results = select_obj_list(Timeline, {"product_id": product_id})
    if len(results) == 0:
        return no_content_204
    products = []
    for result in results:
        products.append(
            {
                "machine_id": result.machine_id,
                "product_id": result.product_id,
                "quantity": result.quantity,
                "time_line": result.time_line,
            }
        )
    return jsonify(products)
