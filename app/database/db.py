import os

from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path(".env")
load_dotenv(override=True, dotenv_path=dotenv_path)

"""
This file get the credentials of mysql database from environmental variable and create the mysql_uri to connect with
the database
"""


db_user = os.getenv("mysql_user")
db_password = os.getenv("mysql_password")
db_host = os.getenv("mysql_host")
mysql_db = os.getenv("vending_db")

print(db_user, db_password, db_host, mysql_db)

mysql_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3308/{mysql_db}"

secret_key = os.getenv("secret_key")
