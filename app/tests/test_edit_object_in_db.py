from typing import Type

from app.database.engine import Session
from app.database.queryUtils import update_database_row_by_id
from app.database.schema import MachineStock, Products, vendingMachine


def setup_object_for_edit(
    table_name: Type[vendingMachine | Products | MachineStock],
    row_object: vendingMachine | Products | MachineStock,
) -> vendingMachine | Products | MachineStock:
    session = Session()
    session.add(row_object)
    session.commit()
    to_be_edited_object = session.query(table_name).first()
    session.close()
    return to_be_edited_object


def clear_db_tables() -> None:
    session = Session()
    session.query(MachineStock).delete()
    session.query(vendingMachine).delete()
    session.query(Products).delete()
    session.commit()
    session.close()


def test_edit_vending_machine() -> None:
    new_vending_machine = vendingMachine("before edit name", "before edit column")
    to_be_edited_vending_machine = setup_object_for_edit(
        vendingMachine, new_vending_machine
    )
    mock_query_strings = {
        "id": to_be_edited_vending_machine.id,
        "machine_name": "after_edit_name",
        "machine_location": "after_edit_location",
    }
    update_database_row_by_id(vendingMachine, mock_query_strings)
    session = Session()
    after_edit_vending_machine = (
        session.query(vendingMachine).filter_by(id=mock_query_strings["id"]).first()
    )
    session.close()
    name_is_edited = (
        after_edit_vending_machine.machine_name == mock_query_strings["machine_name"]
    )
    location_is_edited = (
        after_edit_vending_machine.machine_location
        == mock_query_strings["machine_location"]
    )
    clear_db_tables()
    assert name_is_edited
    assert location_is_edited


def test_edit_product() -> None:
    new_product = Products("before_edit_name", 1, 0, 0)
    to_be_edited_product = setup_object_for_edit(Products, new_product)
    mock_query_strings = {
        "id": to_be_edited_product.id,
        "product_name": "after_edit_name",
        "product_code": 11,
        "product_quantity": 6,
        "price_per_unit": 9,
    }
    update_database_row_by_id(Products, mock_query_strings)
    session = Session()
    after_edit_product = (
        session.query(Products).filter_by(id=mock_query_strings["id"]).first()
    )
    session.close()
    name_is_edited = (
        after_edit_product.product_name == mock_query_strings["product_name"]
    )
    code_is_edited = (
        after_edit_product.product_code == mock_query_strings["product_code"]
    )
    quantity_is_edited = (
        after_edit_product.product_quantity == mock_query_strings["product_quantity"]
    )
    price_is_edited = (
        after_edit_product.price_per_unit == mock_query_strings["price_per_unit"]
    )
    clear_db_tables()
    assert name_is_edited
    assert code_is_edited
    assert quantity_is_edited
    assert price_is_edited


def test_edit_stock() -> None:
    clear_db_tables()
    new_vending_machine = vendingMachine("before edit name", "before edit column")
    new_product = Products("before_edit_name", 1, 1, 1)
    vending_machine_for_stock = setup_object_for_edit(
        vendingMachine, new_vending_machine
    )
    product_for_stock = setup_object_for_edit(Products, new_product)

    new_stock = MachineStock(vending_machine_for_stock.id, product_for_stock.id, 1)
    stock_for_edit = setup_object_for_edit(MachineStock, new_stock)
    mock_query_strings = {"id": stock_for_edit.id, "quantity": 0}
    update_database_row_by_id(MachineStock, mock_query_strings)
    session = Session()
    after_edit_stock = (
        session.query(MachineStock).filter_by(id=mock_query_strings["id"]).first()
    )
    session.close()
    quantity_is_edited = after_edit_stock.quantity == mock_query_strings["quantity"]
    clear_db_tables()
    assert quantity_is_edited
