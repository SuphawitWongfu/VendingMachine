from sqlalchemy import Column, Enum, Numeric, String, Integer, ForeignKey, DateTime, Boolean, Float, Text, MetaData, \
    Table
from app.engine import Engine, Session, Base

"""
This file contain all tables of the database
"""

Base.metadata.create_all(Engine)


# vending machines table
class Vending_machine(Base):
    __tablename__ = 'vending_machines'
    id = Column(Integer, primary_key=True)
    location = Column(String(100))

    def __init__(self, location):
        self.location = location


# consumables table
class Consumables(Base):
    __tablename__ = 'consuamables'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(100))
    product_quantity = Column(Integer)

    def __init__(self, product_name, product_quantity):
        self.product_name = product_name
        self.product_quantity = product_quantity
