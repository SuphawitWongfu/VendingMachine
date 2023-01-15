from app.engine import *
from app.schema import *


def dict_helper(objlist):
    result = [item.obj_to_dict() for item in objlist]
    return result


def getAllFromTable(table_class):
    session = Session()
    queries = session.query(table_class).all()
    session.close()
    return queries


def areAllQueryStringPresent(query_strings, target_sets):
    return all(query_string in query_strings for query_string in target_sets)


def isExist(table_name, search_params):
    session = Session()
    result = session.query(table_name).filter_by(**search_params).first() is not None
    session.close()
    return result


def updateWarehouseQuantity(machine_id, product_id, new_quantity):
        session = Session()
        product_in_warehouse = session.query(Products).filter_by(id=product_id).first()
        product_in_machine = session.query(MachineStock).filter_by(machine_id=machine_id, product_id=product_id).first()
        product_in_warehouse.product_quantity = int(product_in_warehouse.product_quantity) - (
                    int(new_quantity) - int(product_in_machine.quantity))
        session.commit()
        session.close()


def updateDatabaseRowByID(table_class, query_strings):
    session = Session()

    current_item = session.query(table_class).filter_by(id=query_strings["id"]).first()
    for query_string in query_strings.keys():
        setattr(current_item, query_string, query_strings[query_string])
        if type(current_item) is MachineStock and query_string == "quantity":
            print(current_item.machine_id, current_item.product_id, query_strings["quantity"])
            updateWarehouseQuantity(current_item.machine_id, current_item.product_id, query_strings["quantity"])
    session.commit()
    session.close()

