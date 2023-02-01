import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from app.database.queryUtils import add_obj_to_db
from app.database.schema import vendingMachine
from app.tests.conftest import clear_db, get_test_entry, Tester


class MachineTester(Tester):
    def get_all_machines(self) -> TestResponse:
        return self.client.get("/vendings/")


@pytest.fixture
def tester(client: FlaskClient) -> MachineTester:
    return MachineTester(client=client)


def test_view_vending_machine(tester: MachineTester) -> None:
    response = tester.get_all_machines()
    assert Tester.expect(response, 200) or Tester.expect(response, 204)


def test_adding_vending_machine(client: FlaskClient) -> None:
    clear_db(vendingMachine)
    test_data = {"machine_name": "new_edit_name", "machine_location": "new_location"}
    response = client.post(
        "/add_vendings/", query_string=test_data, follow_redirects=True
    )
    assert response.status_code == 200 or response.status_code == 204
    assert len(response.json) != 0


def test_edit_vending_machine(client: FlaskClient) -> None:
    clear_db(vendingMachine)
    add_obj_to_db(vendingMachine("before_edit", "before_edit"))
    test_entry = get_test_entry(vendingMachine)
    test_data = {
        "id": test_entry.id,
        "machine_name": "after_edit_name",
        "machine_location": "after_edit_location",
    }
    response = client.post(
        "/edit_vendings/", query_string=test_data, follow_redirects=True
    )
    edited_test_entry = get_test_entry(vendingMachine)
    assert response.status_code == 200 or response.status_code == 204
    assert len(response.json) != 0
    assert edited_test_entry.id == test_data["id"]
    assert edited_test_entry.machine_name == test_data["machine_name"]
    assert edited_test_entry.machine_location == test_data["machine_location"]


def test_delete_vending_machine(client: FlaskClient) -> None:
    clear_db(vendingMachine)
    add_obj_to_db(vendingMachine("test_name", "test_location"))
    test_entry = get_test_entry(vendingMachine)
    response = client.delete(
        "/delete_vendings/", query_string={"id": test_entry.id}, follow_redirects=True
    )
    assert response.status_code == 200 or response.status_code == 204
    assert response.json is None


def test_failed_add_vending_machine(client: FlaskClient) -> None:
    clear_db(vendingMachine)
    response = client.get("/add_vendings/", query_string={}, follow_redirects=True)
    assert response.status_code == 400


def test_failed_delete_vending_machine(client: FlaskClient) -> None:
    clear_db(vendingMachine)
    response = client.delete(
        "/delete_vendings/", query_string={}, follow_redirects=True
    )
    assert response.status_code == 400
