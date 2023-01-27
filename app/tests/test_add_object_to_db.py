from app.queryUtils import *

def test_add_vending_machine() :
    session = Session()
    new_vending_machine = vendingMachine("test", "test")
    before_add_vending_machine_list = session.query(vendingMachine).all()
    session.close()
    addObjToDB(new_vending_machine)
    session = Session()
    after_add_vending_machine_list = session.query(vendingMachine).all()
    session.query(vendingMachine).delete()
    session.commit()
    session.close()
    assert len(after_add_vending_machine_list) - len(before_add_vending_machine_list) == 1

def test_add_products() :
    session = Session()
    new_product = Products("test_product_name", 1, 10, 10)
    before_add_product_list = session.query(Products).all()
    session.close()
    addObjToDB(new_product)
    session = Session()
    after_add_product_list = session.query(Products).all()
    session.query(Products).delete()
    session.commit()
    session.close()
    assert len(after_add_product_list) - len(before_add_product_list) == 1

def test_add_duplicate_products() :
    new_product = Products("test_product_name", 1, 10, 10)
    addObjToDB(new_product)
    session = Session()
    before_add_duplicate_product_list = session.query(Products).all()
    session.close()
    addObjToDB(new_product)
    session = Session()
    after_add_duplicate_product_list = session.query(Products).all()
    session.query(Products).delete()
    session.commit()
    session.close()
    assert len(after_add_duplicate_product_list) == len(before_add_duplicate_product_list)

def test_add_stock() :
    new_product = Products("test_product_name", 1, 10, 10)
    new_vending_machine = vendingMachine("test", "test")
    addObjToDB(new_product)
    addObjToDB(new_vending_machine)
    session = Session()
    lastest_vending_machine = session.query(vendingMachine).first()
    lastest_product = session.query(Products).first()
    session.close()
    new_stock = MachineStock(lastest_vending_machine.id, lastest_product.id, 5)
    session = Session()
    before_add_stock_list = session.query(MachineStock).all()
    session.close()
    addObjToDB(new_stock)
    session = Session()
    after_add_stock_list = session.query(MachineStock).all()
    session.query(MachineStock).delete()
    session.query(vendingMachine).delete()
    session.query(Products).delete()
    session.commit()
    session.close()
    assert len(after_add_stock_list) - len(before_add_stock_list) == 1





