from flask import Blueprint


stock_timelines = Blueprint("stock_timelines", __name__)


@stock_timelines.route("/get_stock_timelines/", methods=["GET"])
def get_stock_timelines():
    return
