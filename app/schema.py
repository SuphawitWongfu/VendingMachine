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
    name = Column(String(100))
    location = Column(String(100))
    start_service_at = Column(DateTime)

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.start_service_at = dt.datetime.utcnow()


# consumables table
class Consumables(Base):
    __tablename__ = 'consuamables'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(100))
    product_quantity = Column(Integer)

    def __init__(self, product_name, product_quantity):
        self.product_name = product_name
        self.product_quantity = product_quantity
