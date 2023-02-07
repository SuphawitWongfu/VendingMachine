from typing import Dict

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from app.tests.conftest import Tester, clear_db, get_test_entry
from app.database.schema import MachineStock, Products, VendingMachine, Timeline
from app.database.queryUtils import add_obj_to_db


class StockTester(Tester):
    def get_all_stocks(self) -> TestResponse:
        return self.client.get("/machine_stocks/")

    def add_stocks(self, test_data: Dict[str, str | int]) -> TestResponse:
        return self.client.post(
            "/add_machine_stocks/", query_string=test_data, follow_redirects=True
        )

    def delete_stocks(self, test_data: Dict[str, str | int]) -> TestResponse:
        return self.client.delete(
            "/delete_machine_stocks/", query_string=test_data, follow_redirects=True
        )

    def edit_stocks(self, test_data: Dict[str, str | int]) -> TestResponse:
        return self.client.post(
            "/edit_machine_stocks/", query_string=test_data, follow_redirects=True
        )

    def inspect_stock(self) -> TestResponse:
        return self.client.get("/inspect_stocks/")

    def setup_test_env(self):
        clear_db(MachineStock)
        clear_db(Products)
        clear_db(VendingMachine)
        add_obj_to_db(VendingMachine("test_name", "test_loco"))
        add_obj_to_db(Products("test_name", 69, 10, 10))


@pytest.fixture
def tester(client: FlaskClient) -> StockTester:
    return StockTester(client=client)


def test_view_stocks(tester: StockTester) -> None:
    response = tester.get_all_stocks()
    assert tester.expect(response, 200) or tester.expect(response, 204)
    clear_db(Timeline)
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)


def test_add_stocks(tester: StockTester) -> None:
    tester.setup_test_env()
    test_machine = get_test_entry(VendingMachine)
    test_prod = get_test_entry(Products)
    test_data = {
        "machine_id": test_machine.id,
        "product_id": test_prod.id,
        "quantity": 5,
    }
    response = tester.add_stocks(test_data)
    prod_after_added_stock = get_test_entry(Products)
    test_stock = get_test_entry(MachineStock)
    assert tester.expect(response, 200) or tester.expect(response, 204)
    assert prod_after_added_stock.product_quantity + test_stock.quantity == 10
    assert test_stock is not None
    clear_db(Timeline)
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)


def test_add_stocks_fail(tester: StockTester) -> None:
    tester.setup_test_env()
    test_machine = get_test_entry(VendingMachine)
    test_prod = get_test_entry(Products)
    test_data_1 = {"product_id": test_prod.id, "quantity": 5}
    test_data_2 = {
        "machine_id": test_machine.id,
        "product_id": test_prod.id,
        "quantity": -5,
    }
    response_1 = tester.add_stocks(test_data_1)
    response_2 = tester.add_stocks(test_data_2)
    assert tester.expect(response_1, 400)
    assert tester.expect(response_2, 400)
    clear_db(Timeline)
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)


def test_edit_stocks(tester: StockTester) -> None:
    tester.setup_test_env()
    test_machine = get_test_entry(VendingMachine)
    test_prod = get_test_entry(Products)
    add_data = {
        "machine_id": test_machine.id,
        "product_id": test_prod.id,
        "quantity": 5,
    }
    tester.add_stocks(add_data)
    to_be_edit_stock = get_test_entry(MachineStock)
    test_data = {
        "id": to_be_edit_stock.id,
        "machine_id": test_machine.id,
        "product_id": test_prod.id,
        "quantity": 6,
    }
    response = tester.edit_stocks(test_data)
    prod_after_added_stock = get_test_entry(Products)
    test_stock = get_test_entry(MachineStock)
    assert tester.expect(response, 200) or tester.expect(response, 204)
    assert prod_after_added_stock.product_quantity + test_stock.quantity == 10
    assert test_stock.quantity == test_data["quantity"]
    clear_db(Timeline)
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)


def test_edit_stocks_fail(tester: StockTester) -> None:
    tester.setup_test_env()
    test_machine = get_test_entry(VendingMachine)
    test_prod = get_test_entry(Products)
    add_data = {
        "machine_id": test_machine.id,
        "product_id": test_prod.id,
        "quantity": 5,
    }
    tester.add_stocks(add_data)
    to_be_edit_stock = get_test_entry(MachineStock)
    test_data = {
        "machine_id": test_machine.id,
        "product_id": test_prod.id,
        "quantity": 6,
    }
    tester.edit_stocks(test_data)
    prod_after_added_stock = get_test_entry(Products)
    stock_after_edit = get_test_entry(MachineStock)
    assert prod_after_added_stock.product_quantity + stock_after_edit.quantity == 10
    assert to_be_edit_stock.quantity == stock_after_edit.quantity
    clear_db(Timeline)
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)


def test_delete_stocks(tester: StockTester) -> None:
    tester.setup_test_env()
    test_machine = get_test_entry(VendingMachine)
    test_prod = get_test_entry(Products)
    add_data = {
        "machine_id": test_machine.id,
        "product_id": test_prod.id,
        "quantity": 5,
    }
    tester.add_stocks(add_data)
    stock_after_add = get_test_entry(MachineStock)
    assert stock_after_add is not None
    test_data = {"id": get_test_entry(MachineStock).id}
    response = tester.delete_stocks(test_data)
    after_delete_stock = get_test_entry(MachineStock)
    assert tester.expect(response, 200) or tester.expect(response, 204)
    assert after_delete_stock is None
    clear_db(Timeline)
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)


def test_delete_stocks_fail(tester: StockTester) -> None:
    tester.setup_test_env()
    test_machine = get_test_entry(VendingMachine)
    test_prod = get_test_entry(Products)
    add_data = {
        "machine_id": test_machine.id,
        "product_id": test_prod.id,
        "quantity": 5,
    }
    tester.add_stocks(add_data)
    stock_after_add = get_test_entry(MachineStock)
    assert stock_after_add is not None
    test_data = {}
    response = tester.delete_stocks(test_data)
    after_delete_stock = get_test_entry(MachineStock)
    assert tester.expect(response, 400)
    assert after_delete_stock is not None
    clear_db(Timeline)
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)


def test_inspect_stock(tester: StockTester) -> None:
    reponse = tester.inspect_stock()
    assert tester.expect(reponse, 200) or tester.expect(reponse, 204)
