from app.schema import *

'''
this file contains utilities functions for CRUD operation in the database
'''

no_content_204 = '', 204
bad_request_400 = '', 400

'''
this function create a list of dictionaries from a list of objects, queried from the database
objlist - list of objects which was queried from the database
return - a list of dictionaries in which each dictionary is create using obj_to_dict method
'''


def dict_helper(objlist):
    result = [item.obj_to_dict() for item in objlist]
    return result


'''
this function add an object to the database
obj - an object which we wish to add to the database
'''


def addObjToDB(obj):
    if obj is not None:
        session = Session()
        try:
            session.add(obj)
            session.commit()
            session.close()
        except:
            session.close()


'''
this function select a row in the database and return it as object
table_name - the table we wish to query
search_params - a dictionary which structure as {search_key: value_to_search} use to specify search keys while querying
return a row object which was queried from the database if success, else return None
'''


def selectObj(table_name, search_params):
    session = Session()
    obj = None
    try:
        obj = session.query(table_name).filter_by(**search_params).first()
        session.close()
    except:
        session.close()
    return obj


'''
this function query a list of rows from the database and return a list of row objects
table_name - the table we wish to query
search_params - a dictionary which structure as {search_key: value_to_search} use to specify search keys while querying
return a list of row objects which were queried from the database if success, else return None
'''


def selectObjList(table_name, search_params):
    session = Session()
    obj_list = None
    try:
        obj_list = session.query(table_name).filter_by(**search_params).all()
        session.close()
    except:
        session.close()
    return obj_list


'''
this function delete a row from the database based on row obj taking in as the input
obj - a row object which we wish to delete from the database
'''


def deleteObjFromDB(obj):
    if obj is not None:
        session = Session()
        try:
            session.delete(obj)
            session.commit()
            session.close()
        except:
            session.close()


'''
this function query all rows from a specify table
table_class - the table we wish to query
'''


def getAllFromTable(table_class):
    session = Session()
    queries = None
    try:
        queries = session.query(table_class).all()
        session.close()
    except:
        session.close()
    return queries


'''
this function is used to check if all the query strings we need are passed into the url or not
query_strings - the query strings arguments which are passed in the url
target_sets - a set of strings represent all the query strings we want
return true if all the query strings in the target_sets are present in the query_strings
'''


def areAllQueryStringPresent(query_strings, target_sets):
    return all(query_string in query_strings for query_string in target_sets)


'''
this function check if a row is exist in the database or not
table_name - the name of the table we wish to check
search_params - a dictionary which structure as {search_key: value_to_search} use to specify search keys while querying
return true if the row we are trying to check exist in the database and false if not
'''


def isExist(table_name, search_params):
    session = Session()
    result = False
    try:
        result = session.query(table_name).filter_by(**search_params).first() is not None
        session.close()
    except:
        session.close()
    return result


'''
this function updates the product table according to the changes of a product quantity changes in the machine_stock table
product_id - the primary key of the product we wish to update its quantity
quantity_in_machine - the quantity of the product in a vending machine
new_quantity - the new quantity of the product in the machine
return quantity_validation which tells if the update is success or not if success the return 
        the number of that product else return none
'''


def updateWarehouseQuantity(product_id, quantity_in_machine, new_quantity):
    session = Session()
    quantity_validation = None
    try:
        product_in_warehouse = session.query(Products).filter_by(id=product_id).first()
        product_in_warehouse.product_quantity = int(product_in_warehouse.product_quantity) - (
                int(new_quantity) - int(quantity_in_machine))
        if product_in_warehouse.product_quantity >= 0 and int(new_quantity) >= 0 and int(quantity_in_machine) >= 0:
            quantity_validation = product_in_warehouse.product_quantity
            session.commit()
        session.close()
    except:
        session.close()
    return quantity_validation


'''
this function update a row in the database according to the column name specify in query_strings dictionary
table_class - the table we wish to update
query_strings - a dictionary which structure as {search_key: value_to_search} use to specify search keys while querying
'''


def updateDatabaseRowByID(table_class, query_strings):
    session = Session()
    current_item = session.query(table_class).filter_by(id=query_strings["id"]).first()
    if current_item is None:
        return
    for query_string in query_strings.keys():
        setattr(current_item, query_string, query_strings[query_string])
        # case for updating machine_stocks table
        # if type(current_item) is MachineStock and query_string == "quantity":
        # updateWarehouseQuantity(current_item.machine_id, current_item.product_id, query_strings["quantity"])
    session.commit()
    session.close()
