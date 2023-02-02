from dataclasses import dataclass
from typing import Type

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from app.app import create_app
from app.database.engine import Session
from app.database.schema import vendingMachine, MachineStock, Products


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    app.config.update(
        {
            "WTF_CSRF_CHECK_DEFAULT": False,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def clear_db(table_class: Type[vendingMachine | Products | MachineStock]) -> None:
    session = Session()
    session.query(table_class).delete()
    session.commit()
    session.close()


def get_test_entry(
    table_class: Type[vendingMachine | Products | MachineStock],
) -> vendingMachine | Products | MachineStock:
    session = Session()
    test_entry = session.query(table_class).first()
    session.close()
    return test_entry


@dataclass
class Tester:
    __test__ = False
    client: FlaskClient

    @staticmethod
    def expect(response: TestResponse, code: int) -> bool:
        return response.status_code == code
