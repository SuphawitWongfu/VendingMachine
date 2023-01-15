from app.engine import *


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


def updateDatabaseRowByID(table_class, query_strings):
    session = Session()
    try:
        current_item = session.query(table_class).filter_by(id=query_strings["id"]).first()
        for query_string in query_strings.keys():
            setattr(current_item, query_string, query_strings[query_string])
        session.commit()
        session.close()
    except:
        session.close()