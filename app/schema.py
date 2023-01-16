import enum

from sqlalchemy import Column, Enum, Numeric, String, Integer, ForeignKey, DateTime, Boolean, Float, Text, MetaData, \
    Table
from app.engine import Engine, Session, Base
import datetime as dt

"""
This file contain all tables of the database
"""

Base.metadata.create_all(Engine)


# vending machines table
class Vending_machine(Base):
    __tablename__ = 'vending_machines'
    id = Column(Integer, primary_key=True)
    machine_name = Column(String(100))
    machine_location = Column(String(100))
    installed_at = Column(DateTime)

    def __init__(self, name, location):
        self.machine_name = name
        self.machine_location = location
        self.installed_at = dt.datetime.utcnow()

    def obj_to_dict(self):
        query_dict = {
            "id": self.id,
            "name": self.machine_name,
            "location": self.machine_location,
            "installed_at": self.installed_at
        }
        return query_dict


# consumables table
class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(100))
    product_code = Column(Integer, unique=True)
    product_quantity = Column(Integer)
    price_per_unit = Column(Float)

    def __init__(self, product_name, product_code, product_quantity, price_per_unit):
        self.product_name = product_name
        self.product_quantity = product_quantity
        self.product_code = product_code
        self.price_per_unit = price_per_unit

    def obj_to_dict(self):
        query_dict = {
            "id": self.id,
            "product_name": self.product_name,
            "product_quantity": self.product_quantity,
            "product_code": self.product_code,
            "price_per_unit": self.price_per_unit
        }
        return query_dict


class MachineStock(Base):
    __tablename__ = "machine_stocks"
    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('vending_machines.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    def __init__(self, machine_id, product_id, quantity):
        self.machine_id = machine_id
        self.product_id = product_id
        self.quantity = quantity

    def obj_to_dict(self):
        query_dict = {
            "id": self.id,
            "machine_id": self.machine_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        }
        return query_dict
