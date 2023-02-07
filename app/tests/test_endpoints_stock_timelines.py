from typing import Dict

from flask.testing import FlaskClient

import pytest

from app.database.schema import VendingMachine, Products, Timeline, MachineStock
from app.tests.conftest import Tester, get_test_entry, clear_db
from werkzeug.test import TestResponse

from app.tests.test_endpoints_machine_stock import StockTester


class TimelineTester(Tester):
    def get_all_product_stamp(self, test_data: Dict[str, int]) -> TestResponse:
        return self.client.get(
            "/get_product_timestamps/", query_string=test_data, follow_redirects=True
        )

    def get_all_quantity_stamp(self, test_data: Dict[str, int]) -> TestResponse:
        return self.client.get(
            "/get_quantity_timestamps/", query_string=test_data, follow_redirects=True
        )


@pytest.fixture
def timeline_tester(client: FlaskClient) -> TimelineTester:
    return TimelineTester(client=client)


@pytest.fixture
def stock_tester(client: FlaskClient) -> StockTester:
    return StockTester(client=client)


def test_get_all_product_stamp(
    timeline_tester: TimelineTester, stock_tester: StockTester
):
    stock_tester.setup_test_env()
    test_machine = get_test_entry(VendingMachine)
    test_prod = get_test_entry(Products)
    test_data = {
        "machine_id": test_machine.id,
        "product_id": test_prod.id,
        "quantity": 5,
    }
    stock_tester.add_stocks(test_data)
    response = timeline_tester.get_all_product_stamp({"machine_id": test_machine.id})
    assert response.status_code == 200
    clear_db(Timeline)
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)


def test_get_quantity_timestamps(
    timeline_tester: TimelineTester, stock_tester: StockTester
):
    stock_tester.setup_test_env()
    test_machine = get_test_entry(VendingMachine)
    test_prod = get_test_entry(Products)
    test_data = {
        "machine_id": test_machine.id,
        "product_id": test_prod.id,
        "quantity": 5,
    }
    stock_tester.add_stocks(test_data)
    response = timeline_tester.get_all_quantity_stamp({"product_id": test_prod.id})
    assert response.status_code == 200
    clear_db(Timeline)
    clear_db(MachineStock)
    clear_db(Products)
    clear_db(VendingMachine)
