from flask import Blueprint, request, jsonify, Response

from app.database.queryUtils import select_obj_list
from app.database.schema import Timeline

stock_timelines = Blueprint("stock_timelines", __name__)


@stock_timelines.route("/get_product_timestamps/", methods=["GET"])
def get_product_timestamps() -> Response:
    query_strings = request.args
    machine_id = query_strings["machine_id"]
    return jsonify(select_obj_list(Timeline, {"machine_id": machine_id}))


@stock_timelines.route("/get_quantity_timestamps/", methods=["GET"])
def get_quantity_timestamps() -> Response:
    query_strings = request.args
    product_id = query_strings["product_id"]
    return jsonify(select_obj_list(Timeline, {"product_id": product_id}))
