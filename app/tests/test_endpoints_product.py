from typing import Dict

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from app.tests.conftest import Tester, clear_db, get_test_entry
from app.database.schema import Products


class ProductTester(Tester):
    def get_all_products(self) -> TestResponse:
        return self.client.get("/products/")

    def add_product(self, test_data: Dict[str, str | int]) -> TestResponse:
        return self.client.post(
            "/add_products/", query_string=test_data, follow_redirects=True
        )

    def delete_product(self, test_data: Dict[str, str | int]) -> TestResponse:
        return self.client.delete(
            "/delete_products/", query_string=test_data, follow_redirects=True
        )

    def edit_product(self, test_data: Dict[str, str | int]) -> TestResponse:
        return self.client.post(
            "/edit_products/", query_string=test_data, follow_redirects=True
        )


@pytest.fixture
def tester(client: FlaskClient) -> ProductTester:
    return ProductTester(client=client)


def test_view_products(tester: ProductTester) -> None:
    response = tester.get_all_products()
    assert Tester.expect(response, 200) or Tester.expect(response, 204)
    clear_db(Products)


def test_add_product(tester: ProductTester) -> None:
    clear_db(Products)
    test_data = {
        "product_name": "test_product",
        "product_code": 69,
        "product_quantity": 5,
        "price_per_unit": 10,
    }
    response = tester.add_product(test_data)
    assert Tester.expect(response, 200) or Tester.expect(response, 204)
    assert len(response.json) != 0
    clear_db(Products)


def test_add_product_fail(tester: ProductTester) -> None:
    response = tester.add_product({})
    assert Tester.expect(response, 400)
    clear_db(Products)


def test_edit_product(tester: ProductTester) -> None:
    clear_db(Products)
    add_data = {
        "product_name": "test_product",
        "product_code": 69,
        "product_quantity": 5,
        "price_per_unit": 10,
    }
    tester.add_product(add_data)
    to_be_edit_prod = get_test_entry(Products)
    test_data = {
        "id": to_be_edit_prod.id,
        "product_name": "after_edit",
        "product_code": 0,
        "product_quantity": 0,
        "price_per_unit": 0,
    }
    response = tester.edit_product(test_data)
    after_edit_prod = get_test_entry(Products)
    assert Tester.expect(response, 200) or Tester.expect(response, 204)
    assert after_edit_prod.product_name == test_data["product_name"]
    assert after_edit_prod.product_quantity == test_data["product_quantity"]
    assert after_edit_prod.product_code == test_data["product_code"]
    assert after_edit_prod.price_per_unit == test_data["price_per_unit"]
    clear_db(Products)


def test_edit_product_fail(tester: ProductTester) -> None:
    clear_db(Products)
    add_data = {
        "product_name": "test_product",
        "product_code": 69,
        "product_quantity": 5,
        "price_per_unit": 10,
    }
    tester.add_product(add_data)
    to_be_edit_prod = get_test_entry(Products)
    test_data = {
        "product_name": "after_edit",
        "product_code": 0,
        "product_quantity": 0,
        "price_per_unit": 0,
    }
    tester.edit_product(test_data)
    after_edit_prod = get_test_entry(Products)
    assert after_edit_prod.product_name == to_be_edit_prod.product_name
    assert after_edit_prod.product_quantity == to_be_edit_prod.product_quantity
    assert after_edit_prod.product_code == to_be_edit_prod.product_code
    assert after_edit_prod.price_per_unit == to_be_edit_prod.price_per_unit
    clear_db(Products)


def test_delete_product(tester: ProductTester) -> None:
    clear_db(Products)
    add_data = {
        "product_name": "test_product",
        "product_code": 69,
        "product_quantity": 5,
        "price_per_unit": 10,
    }
    tester.add_product(add_data)
    to_be_delete_prod = get_test_entry(Products)
    test_data = {"id": to_be_delete_prod.id}
    response = tester.delete_product(test_data)
    after_delete_prod = get_test_entry(Products)
    assert Tester.expect(response, 200) or Tester.expect(response, 204)
    assert after_delete_prod is None
    clear_db(Products)


def test_db_delete_product_fail(tester: ProductTester) -> None:
    clear_db(Products)
    add_data = {
        "product_name": "test_product",
        "product_code": 69,
        "product_quantity": 5,
        "price_per_unit": 10,
    }
    tester.add_product(add_data)
    test_data = {}
    response = tester.delete_product(test_data)
    after_delete_prod = get_test_entry(Products)
    assert Tester.expect(response, 400)
    assert after_delete_prod is not None
    clear_db(Products)
