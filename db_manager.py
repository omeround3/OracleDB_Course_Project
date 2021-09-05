from config import db_connection
import os
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=os.environ.get("HOME")+"/Downloads/instantclient_19_8")

# Create Oracle DB connecton and return a cursor
def connect():
    connection = cx_Oracle.connect(db_connection['db_user'], db_connection['db_password'], db_connection['db_url'])
    print("Database version:", connection.version)
    print("Client version:", cx_Oracle.clientversion())
    print("Successfully connected to Oracle Database")

    return connection.cursor()

    