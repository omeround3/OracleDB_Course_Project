from config import db_connection
import os
import sys
import cx_Oracle as oracledb
from flask import current_app

################################################################################
#
# On macOS tell cx_Oracle 8 where the Instant Client libraries are.  You can do
# the same on Windows, or add the directories to PATH.  On Linux, use ldconfig
# or LD_LIBRARY_PATH.  cx_Oracle installation instructions are at:
# https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
if sys.platform.startswith("darwin"):
    oracledb.init_oracle_client(lib_dir=os.environ.get(
        "HOME")+"/Downloads/instantclient_19_8")
elif sys.platform.startswith("win32"):
    oracledb.init_oracle_client(lib_dir=r"c:\oracle\instantclient_19_8")

################################################################################
#

# pool = oracledb.SessionPool(db_connection['db_user'], db_connection['db_password'],
                                    # db_connection['db_url'], min=2, max=5, increment=1, encoding="UTF-8")


def connect():
    """ Create Oracle DB connecton and return a cursor """
    try:
        connection = oracledb.connect(
            db_connection['db_user'], db_connection['db_password'], db_connection['db_url'])
        print("Database version:", connection.version)
        print("Client version:", oracledb.clientversion())
        print("Successfully connected to Oracle Database")
        return connection
    except oracledb.DatabaseError as e:
        error = e.args
        if error.code == 1017:
            print('Username/Password invaild.')
            # logger.debug("Username/password invalid: %s", error.code)
        else:
            # logger.debug("Database connection error: %s", e)
            print("Database connection error: %s".format(e))
        raise


def init_db():
    """ Initalize DB function """
    db = connect()

    with current_app.open_resource('DB_Files/Committe_DB_DDL_v3_WITH_DROP_test.ddl') as init_db_script:
        db.execute(init_db_script.read().decode('utf8'))

    db.close()


def output_type_handler(cursor, name, default_type, size, precision, scale):
    """ Handling CLOB & BLOB operations in the database."""
    if default_type == oracledb.CLOB:
        return cursor.var(oracledb.LONG_STRING, arraysize=cursor.arraysize)
    if default_type == oracledb.BLOB:
        return cursor.var(oracledb.LONG_BINARY, arraysize=cursor.arraysize)
