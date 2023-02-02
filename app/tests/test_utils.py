from app.database.queryUtils import update_warehouse_quantity, add_obj_to_db
from app.tests.conftest import clear_db, get_test_entry
from app.database.schema import MachineStock, VendingMachine, Products
from app.endpoints.machine_stocks import create_listing


def setup_test_env():
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)
    add_obj_to_db(VendingMachine("test_name", "test_loco"))
    add_obj_to_db(Products("test_name", 69, 10, 10))


def test_update_warehouse_quantity():
    setup_test_env()
    test_product = get_test_entry(Products)
    validation = update_warehouse_quantity(test_product.id, 5, 7)
    assert validation == 8
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)


def test_create_listing():
    setup_test_env()
    test_machine = get_test_entry(VendingMachine)
    test_product = get_test_entry(Products)
    add_obj_to_db(MachineStock(test_machine.id, test_product.id, 5))
    data = create_listing(test_machine.id)
    assert data is not None
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)
