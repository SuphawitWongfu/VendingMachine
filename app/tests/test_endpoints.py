from flask.testing import FlaskClient


def test_view_vending_machine(client: FlaskClient) -> None:
    response = client.get("/vendings/")
    assert response.status_code == 200 or response.status_code == 204


def test_view_product(client: FlaskClient) -> None:
    response = client.get("/products/")
    assert response.status_code == 200 or response.status_code == 204


def test_view_machine_stock(client: FlaskClient) -> None:
    response = client.get("/machine_stocks/")
    assert response.status_code == 200 or response.status_code == 204
