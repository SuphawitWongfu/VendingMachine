from typing import Type

from flask.testing import FlaskClient

from app.database.engine import Session
from app.database.queryUtils import add_obj_to_db
from app.database.schema import vendingMachine


def clear_db() -> None:
    session = Session()
    session.query(vendingMachine).delete()
    session.commit()
    session.close()


def get_test_entry() -> Type[vendingMachine]:
    session = Session()
    test_entry = session.query(vendingMachine).first()
    session.close()
    return test_entry


def test_view_vending_machine(client: FlaskClient):
    response = client.get("/vendings/")
    assert response.status_code == 200 or response.status_code == 204


def test_adding_vending_machine(client: FlaskClient):
    clear_db()
    test_data = {"machine_name": "new_edit_name", "machine_location": "new_location"}
    response = client.post(
        "/add_vendings/", query_string=test_data, follow_redirects=True
    )
    assert response.status_code == 200 or response.status_code == 204
    assert len(response.json) != 0


def test_edit_vending_machine(client: FlaskClient):
    clear_db()
    add_obj_to_db(vendingMachine("before_edit", "before_edit"))
    test_entry = get_test_entry()
    test_data = {
        "id": test_entry.id,
        "machine_name": "after_edit_name",
        "machine_location": "after_edit_location",
    }
    response = client.post(
        "/edit_vendings/", query_string=test_data, follow_redirects=True
    )
    edited_test_entry = get_test_entry()
    assert response.status_code == 200 or response.status_code == 204
    assert len(response.json) != 0
    assert edited_test_entry.id == test_data["id"]
    assert edited_test_entry.machine_name == test_data["machine_name"]
    assert edited_test_entry.machine_location == test_data["machine_location"]


def test_delete_vending_machine(client: FlaskClient):
    clear_db()
    add_obj_to_db(vendingMachine("test_name", "test_location"))
    test_entry = get_test_entry()
    response = client.delete(
        "/delete_vendings/", query_string={"id": test_entry.id}, follow_redirects=True
    )
    assert response.status_code == 200 or response.status_code == 204
    assert response.json is None


def test_failed_add_vending_machine(client: FlaskClient):
    clear_db()
    response = client.get("/add_vendings/", query_string={}, follow_redirects=True)
    assert response.status_code == 400


def test_failed_delete_vending_machine(client: FlaskClient):
    clear_db()
    response = client.delete(
        "/delete_vendings/", query_string={}, follow_redirects=True
    )
    assert response.status_code == 400
