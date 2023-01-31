from typing import Type

from app.database.engine import Session
from app.database.queryUtils import delete_obj_from_db
from app.database.schema import MachineStock, Products, vendingMachine


def setup_db_for_delete(
    table_name: Type[vendingMachine | Products | MachineStock],
    row_object: vendingMachine | Products | MachineStock,
) -> Type[vendingMachine | Products | MachineStock]:
    session = Session()
    session.add(row_object)
    session.commit()
    unwanted_object = session.query(table_name).first()
    session.close()
    return unwanted_object


def test_delete_vending_machine() -> None:
    unwanted_vending_machine = setup_db_for_delete(
        vendingMachine, vendingMachine("testname", "testlocation")
    )
    assert unwanted_vending_machine is not None
    delete_obj_from_db(unwanted_vending_machine)
    session = Session()
    unwanted_vending_machine_after_delete = (
        session.query(vendingMachine).filter_by(id=unwanted_vending_machine.id).first()
    )
    assert unwanted_vending_machine_after_delete is None


def test_delete_product() -> None:
    unwanted_product = setup_db_for_delete(Products, Products("test_product", 1, 1, 1))
    assert unwanted_product is not None
    delete_obj_from_db(unwanted_product)
    session = Session()
    unwanted_product_after_delete = (
        session.query(vendingMachine).filter_by(id=unwanted_product.id).first()
    )
    assert unwanted_product_after_delete is None


def test_delete_stock() -> None:
    unwanted_product = setup_db_for_delete(Products, Products("test_product", 1, 1, 1))
    unwanted_vending_machine = setup_db_for_delete(
        vendingMachine, vendingMachine("testname", "testlocation")
    )
    unwanted_stock = setup_db_for_delete(
        MachineStock, MachineStock(unwanted_vending_machine.id, unwanted_product.id, 1)
    )
    assert unwanted_stock is not None
    delete_obj_from_db(unwanted_stock)
    session = Session()
    unwanted_stock_after_delete = (
        session.query(vendingMachine).filter_by(id=unwanted_stock.id).first()
    )
    session.query(Products).delete()
    session.query(vendingMachine).delete()
    session.commit()
    assert unwanted_stock_after_delete is None
