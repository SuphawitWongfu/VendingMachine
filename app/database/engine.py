from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.database.db import mysql_uri

"""
This file contains the logic of creating sqlalchemy database engine
"""

Engine = create_engine(mysql_uri, echo=True)
Session = sessionmaker(bind=Engine)
Base = declarative_base()
