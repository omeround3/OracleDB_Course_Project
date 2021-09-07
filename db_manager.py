from config import db_connection
import os
import sys
import cx_Oracle
import click
from flask import current_app
from flask.cli import with_appcontext

################################################################################
#
# On macOS tell cx_Oracle 8 where the Instant Client libraries are.  You can do
# the same on Windows, or add the directories to PATH.  On Linux, use ldconfig
# or LD_LIBRARY_PATH.  cx_Oracle installation instructions are at:
# https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
if sys.platform.startswith("darwin"):
    cx_Oracle.init_oracle_client(lib_dir=os.environ.get(
        "HOME")+"/Downloads/instantclient_19_8")
elif sys.platform.startswith("win32"):
    cx_Oracle.init_oracle_client(lib_dir=r"c:\oracle\instantclient_19_8")

################################################################################
#


# Create Oracle DB connecton and return a cursor
def connect():
    connection = cx_Oracle.connect(
        db_connection['db_user'], db_connection['db_password'], db_connection['db_url'])
    print("Database version:", connection.version)
    print("Client version:", cx_Oracle.clientversion())
    print("Successfully connected to Oracle Database")

    return connection.cursor()


def init_db():
    db = connect()

    with current_app.open_resource('DB_Files/Committe_DB_DDL_v3_WITH_DROP.ddl') as init_db_script:
        db.execute(init_db_script.read().decode('utf-8'))

    db.close()


# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')

