"""This file contain all tables of the database."""

import datetime as dt
from dataclasses import dataclass
from typing import Dict

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, JSON

from app.database.engine import Base, Engine

Base.metadata.create_all(Engine)


class VendingMachine(Base):
    """A class represents vending_machine table in the database."""

    __tablename__ = "vending_machines"
    id = Column(Integer, primary_key=True)
    machine_name = Column(String(100))
    machine_location = Column(String(100))
    installed_at = Column(DateTime)

    def __init__(self, name: str, location: str):  # noqa: ANN204
        self.machine_name = name
        self.machine_location = location
        self.installed_at = dt.datetime.utcnow()

    def obj_to_dict(self) -> Dict[str, str]:
        query_dict = {
            "id": self.id,
            "name": self.machine_name,
            "location": self.machine_location,
            "installed_at": self.installed_at,
        }
        return query_dict


class Products(Base):
    """A class represents products table in the database."""

    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    product_name = Column(String(100))
    product_code = Column(Integer, unique=True)
    product_quantity = Column(Integer)
    price_per_unit = Column(Float)

    def __init__(
        self,
        product_name: str,
        product_code: int,
        product_quantity: int,
        price_per_unit: int,
    ):  # noqa: ANN204
        self.product_name = product_name
        self.product_quantity = product_quantity
        self.product_code = product_code
        self.price_per_unit = price_per_unit

    def obj_to_dict(self) -> Dict[str, str]:
        query_dict = {
            "id": self.id,
            "product_name": self.product_name,
            "product_quantity": self.product_quantity,
            "product_code": self.product_code,
            "price_per_unit": self.price_per_unit,
        }
        return query_dict


class MachineStock(Base):
    """A class represents machine_stocks table in the database."""

    __tablename__ = "machine_stocks"
    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey("vending_machines.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    def __init__(self, machine_id: int, product_id: int, quantity: int):  # noqa: ANN204
        self.machine_id = machine_id
        self.product_id = product_id
        self.quantity = quantity

    def obj_to_dict(self) -> Dict[str, int]:
        query_dict = {
            "id": self.id,
            "machine_id": self.machine_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
        }
        return query_dict


@dataclass
class Timeline(Base):
    machine_id: int
    product_id: int
    method: str
    machine_state: JSON
    time_line: DateTime

    __tablename__ = "machine_timeline"
    id = Column(Integer, primary_key=True)
    machine_id = Column(
        Integer,
        ForeignKey("vending_machines.id"),
        nullable=False,
    )
    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
    )
    method = Column(String(100), nullable=False)
    machine_state = Column(JSON, nullable=True)
    time_line = Column(DateTime)
