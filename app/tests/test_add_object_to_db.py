"""test adding object to database."""
from app.database.engine import Session
from app.database.queryUtils import add_obj_to_db
from app.database.schema import MachineStock, Products, vendingMachine
from app.tests.conftest import create_app


create_app()


def test_add_vending_machine() -> None:
    """Test adding vending machine object."""
    session = Session()
    new_vending_machine = vendingMachine("test", "test")
    before_add_vending_machine_list = session.query(vendingMachine).all()
    session.close()
    add_obj_to_db(new_vending_machine)
    session = Session()
    after_add_vending_machine_list = session.query(vendingMachine).all()
    session.query(vendingMachine).delete()
    session.commit()
    session.close()
    assert (
        len(after_add_vending_machine_list) - len(before_add_vending_machine_list) == 1
    )


def test_add_products() -> None:
    """Test adding products object."""
    session = Session()
    new_product = Products("test_product_name", 1, 10, 10)
    before_add_product_list = session.query(Products).all()
    session.close()
    add_obj_to_db(new_product)
    session = Session()
    after_add_product_list = session.query(Products).all()
    session.query(Products).delete()
    session.commit()
    session.close()
    assert len(after_add_product_list) - len(before_add_product_list) == 1


def test_add_duplicate_products() -> None:
    """Test adding duplicate product object."""
    new_product = Products("test_product_name", 1, 10, 10)
    add_obj_to_db(new_product)
    session = Session()
    before_add_duplicate_product_list = session.query(Products).all()
    session.close()
    add_obj_to_db(new_product)
    session = Session()
    after_add_duplicate_product_list = session.query(Products).all()
    session.query(Products).delete()
    session.commit()
    session.close()
    assert len(after_add_duplicate_product_list) == len(
        before_add_duplicate_product_list
    )


def test_add_stock() -> None:
    """Test adding machine stock object."""
    new_product = Products("test_product_name", 1, 10, 10)
    new_vending_machine = vendingMachine("test", "test")
    add_obj_to_db(new_product)
    add_obj_to_db(new_vending_machine)
    session = Session()
    lastest_vending_machine = session.query(vendingMachine).first()
    lastest_product = session.query(Products).first()
    session.close()
    new_stock = MachineStock(lastest_vending_machine.id, lastest_product.id, 5)
    session = Session()
    before_add_stock_list = session.query(MachineStock).all()
    session.close()
    add_obj_to_db(new_stock)
    session = Session()
    after_add_stock_list = session.query(MachineStock).all()
    session.query(MachineStock).delete()
    session.query(vendingMachine).delete()
    session.query(Products).delete()
    session.commit()
    session.close()
    assert len(after_add_stock_list) - len(before_add_stock_list) == 1
