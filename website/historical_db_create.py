from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'PP1_historical'

TABLES = {}
TABLES['historical_AMZN'] = (
    "CREATE TABLE `historical_AMZN` ("
    "  `stock_name` Character(100) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `open` Double NOT NULL,"
    "  `high` Double NOT NULL,"
    "  `low` Double NOT NULL,"
    "  `close` Double NOT NULL,"
    "  `volume` Double NOT NULL,"
    "  PRIMARY KEY (date)"
    ") ENGINE=InnoDB")
TABLES['historical_PETX'] = (
    "CREATE TABLE `historical_PETX` ("
    "  `stock_name` Character(100) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `open` Double NOT NULL,"
    "  `high` Double NOT NULL,"
    "  `low` Double NOT NULL,"
    "  `close` Double NOT NULL,"
    "  `volume` Double NOT NULL,"
    "  PRIMARY KEY (date)"
    ") ENGINE=InnoDB")

TABLES['historical_AABA'] = (
    "CREATE TABLE `historical_AABA` ("
    "  `stock_name` Character(100) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `open` Double NOT NULL,"
    "  `high` Double NOT NULL,"
    "  `low` Double NOT NULL,"
    "  `close` Double NOT NULL,"
    "  `volume` Double NOT NULL,"
    "  PRIMARY KEY (date)"
    ") ENGINE=InnoDB")

TABLES['historical_NVDA'] = (
    "CREATE TABLE `historical_NVDA` ("
    "  `stock_name` Character(100) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `open` Double NOT NULL,"
    "  `high` Double NOT NULL,"
    "  `low` Double NOT NULL,"
    "  `close` Double NOT NULL,"
    "  `volume` Double NOT NULL,"
    "  PRIMARY KEY (date)"
    ") ENGINE=InnoDB")
TABLES['historical_TXN'] = (
    "CREATE TABLE `historical_TXN` ("
    "  `stock_name` Character(100) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `open` Double NOT NULL,"
    "  `high` Double NOT NULL,"
    "  `low` Double NOT NULL,"
    "  `close` Double NOT NULL,"
    "  `volume` Double NOT NULL,"
    "  PRIMARY KEY (date)"
    ") ENGINE=InnoDB")
TABLES['historical_NDAQ'] = (
    "CREATE TABLE `historical_NDAQ` ("
    "  `stock_name` Character(100) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `open` Double NOT NULL,"
    "  `high` Double NOT NULL,"
    "  `low` Double NOT NULL,"
    "  `close` Double NOT NULL,"
    "  `volume` Double NOT NULL,"
    "  PRIMARY KEY (date)"
    ") ENGINE=InnoDB")
TABLES['historical_GOOG'] = (
    "CREATE TABLE `historical_GOOG` ("
    "  `stock_name` Character(100) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `open` Double NOT NULL,"
    "  `high` Double NOT NULL,"
    "  `low` Double NOT NULL,"
    "  `close` Double NOT NULL,"
    "  `volume` Double NOT NULL,"
    "  PRIMARY KEY (date)"
    ") ENGINE=InnoDB")
TABLES['historical_FB'] = (
    "CREATE TABLE `historical_FB` ("
    "  `stock_name` Character(100) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `open` Double NOT NULL,"
    "  `high` Double NOT NULL,"
    "  `low` Double NOT NULL,"
    "  `close` Double NOT NULL,"
    "  `volume` Double NOT NULL,"
    "  PRIMARY KEY (date)"
    ") ENGINE=InnoDB")
TABLES['historical_GS'] = (
    "CREATE TABLE `historical_GS` ("
    "  `stock_name` Character(100) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `open` Double NOT NULL,"
    "  `high` Double NOT NULL,"
    "  `low` Double NOT NULL,"
    "  `close` Double NOT NULL,"
    "  `volume` Double NOT NULL,"
    "  PRIMARY KEY (date)"
    ") ENGINE=InnoDB")
TABLES['historical_AAPL'] = (
    "CREATE TABLE `historical_AAPL` ("
    "  `stock_name` Character(100) NOT NULL,"
    "  `date` date NOT NULL,"
    "  `open` Double NOT NULL,"
    "  `high` Double NOT NULL,"
    "  `low` Double NOT NULL,"
    "  `close` Double NOT NULL,"
    "  `volume` Double NOT NULL,"
    "  PRIMARY KEY (date)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='george',password='george')
cursor = cnx.cursor()
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)
for name, ddl in TABLES.items():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
