from app.queryUtils import *

def setup_db_for_delete(table_name, row_object) :
    session = Session()
    session.add(row_object)
    session.commit()
    unwanted_object = session.query(table_name).first()
    session.close()
    return  unwanted_object

def test_delete_vending_machine() :
    unwanted_vending_machine = setup_db_for_delete(vendingMachine, vendingMachine("testname", "testlocation"))
    assert unwanted_vending_machine is not None
    deleteObjFromDB(unwanted_vending_machine)
    session = Session()
    unwanted_vending_machine_after_delete = session.query(vendingMachine).filter_by(id=unwanted_vending_machine.id).first()
    assert unwanted_vending_machine_after_delete is None

def test_delete_product() :
    unwanted_product = setup_db_for_delete(Products, Products("test_product", 1, 1 ,1))
    assert unwanted_product is not None
    deleteObjFromDB(unwanted_product)
    session = Session()
    unwanted_product_after_delete = session.query(vendingMachine).filter_by(id=unwanted_product.id).first()
    assert unwanted_product_after_delete is None

def test_delete_stock() :
    unwanted_product = setup_db_for_delete(Products, Products("test_product", 1, 1 ,1))
    unwanted_vending_machine = setup_db_for_delete(vendingMachine, vendingMachine("testname", "testlocation"))
    unwanted_stock = setup_db_for_delete(MachineStock, MachineStock(unwanted_vending_machine.id, unwanted_product.id, 1))
    assert unwanted_stock is not None
    deleteObjFromDB(unwanted_stock)
    session = Session()
    unwanted_stock_after_delete = session.query(vendingMachine).filter_by(id=unwanted_stock.id).first()
    session.query(Products).delete()
    session.query(vendingMachine).delete()
    session.commit()
    assert unwanted_stock_after_delete is None



