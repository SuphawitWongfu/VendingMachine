import os

from app.credentials import prepare_credentials

"""
This file get the credentials of mysql database from environmental variable and create the mysql_uri to connect with
the database
"""

prepare_credentials()

db_user = os.environ.get("mysql_user")
db_password = os.environ.get("mysql_password")
db_host = os.environ.get("mysql_host")
db_port = os.environ.get("mysql_port")
mysql_db = os.environ.get("vending_db")

mysql_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{mysql_db}"
