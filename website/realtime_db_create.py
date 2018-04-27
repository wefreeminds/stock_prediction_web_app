from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import csv

DB_NAME = 'PP1_real_time'
stock_names =['AMZN', 'PETX', 'AABA', 'AAPL', 'NVDA','TXN', 'NDAQ', 'GOOG', 'FB', 'GS']
#for stock_name in stock_names:
#	with open('A:/'+stock_name+'.csv', 'w') as outcsv:
#		fieldnames=["name","date","open","high","low","close","volume"]
#		writer = csv.DictWriter(outcsv,fieldnames=fieldnames)
#		writer.writeheader()

TABLES = {}

TABLES['realtime_AMZN'] = (
	"CREATE TABLE `realtime_AMZN` ("
	"  `stock_name` Character(100) NOT NULL,"
	"  `datetime` datetime NOT NULL,"
	"  `open` Double NOT NULL,"
	"  `high` Double NOT NULL,"
	"  `low` Double NOT NULL,"
	"  `close` Double NOT NULL,"
	"  `volume` Double NOT NULL,"
	"  PRIMARY KEY (datetime)"
	") ENGINE=InnoDB")
TABLES['realtime_PETX'] = (
	"CREATE TABLE `realtime_PETX` ("
	"  `stock_name` Character(100) NOT NULL,"
	"  `datetime` datetime NOT NULL,"
	"  `open` Double NOT NULL,"
	"  `high` Double NOT NULL,"
	"  `low` Double NOT NULL,"
	"  `close` Double NOT NULL,"
	"  `volume` Double NOT NULL,"
	"  PRIMARY KEY (datetime)"
	") ENGINE=InnoDB")

TABLES['realtime_GOOG'] = (
	"CREATE TABLE `realtime_GOOG` ("
	"  `stock_name` Character(100) NOT NULL,"
	"  `datetime` datetime NOT NULL,"
	"  `open` Double NOT NULL,"
	"  `high` Double NOT NULL,"
	"  `low` Double NOT NULL,"
	"  `close` Double NOT NULL,"
	"  `volume` Double NOT NULL,"
	"  PRIMARY KEY (datetime)"
	") ENGINE=InnoDB")

TABLES['realtime_NVDA'] = (
	"CREATE TABLE `realtime_NVDA` ("
	"  `stock_name` Character(100) NOT NULL,"
	"  `datetime` datetime NOT NULL,"
	"  `open` Double NOT NULL,"
	"  `high` Double NOT NULL,"
	"  `low` Double NOT NULL,"
	"  `close` Double NOT NULL,"
	"  `volume` Double NOT NULL,"
	"  PRIMARY KEY (datetime)"
	") ENGINE=InnoDB")
TABLES['realtime_TXN'] = (
	"CREATE TABLE `realtime_TXN` ("
	"  `stock_name` Character(100) NOT NULL,"
	"  `datetime` datetime NOT NULL,"
	"  `open` Double NOT NULL,"
	"  `high` Double NOT NULL,"
	"  `low` Double NOT NULL,"
	"  `close` Double NOT NULL,"
	"  `volume` Double NOT NULL,"
	"  PRIMARY KEY (datetime)"
	") ENGINE=InnoDB")
TABLES['realtime_NDAQ'] = (
	"CREATE TABLE `realtime_NDAQ` ("
	"  `stock_name` Character(100) NOT NULL,"
	"  `datetime` datetime NOT NULL,"
	"  `open` Double NOT NULL,"
	"  `high` Double NOT NULL,"
	"  `low` Double NOT NULL,"
	"  `close` Double NOT NULL,"
	"  `volume` Double NOT NULL,"
	"  PRIMARY KEY (datetime)"
	") ENGINE=InnoDB")
TABLES['realtime_AABA'] = (
	"CREATE TABLE `realtime_AABA` ("
	"  `stock_name` Character(100) NOT NULL,"
	"  `datetime` datetime NOT NULL,"
	"  `open` Double NOT NULL,"
	"  `high` Double NOT NULL,"
	"  `low` Double NOT NULL,"
	"  `close` Double NOT NULL,"
	"  `volume` Double NOT NULL,"
	"  PRIMARY KEY (datetime)"
	") ENGINE=InnoDB")
TABLES['realtime_FB'] = (
	"CREATE TABLE `realtime_FB` ("
	"  `stock_name` Character(100) NOT NULL,"
	"  `datetime` datetime NOT NULL,"
	"  `open` Double NOT NULL,"
	"  `high` Double NOT NULL,"
	"  `low` Double NOT NULL,"
	"  `close` Double NOT NULL,"
	"  `volume` Double NOT NULL,"
	"  PRIMARY KEY (datetime)"
	") ENGINE=InnoDB")
TABLES['realtime_GS'] = (
	"CREATE TABLE `realtime_GS` ("
	"  `stock_name` Character(100) NOT NULL,"
	"  `datetime` datetime NOT NULL,"
	"  `open` Double NOT NULL,"
	"  `high` Double NOT NULL,"
	"  `low` Double NOT NULL,"
	"  `close` Double NOT NULL,"
	"  `volume` Double NOT NULL,"
	"  PRIMARY KEY (datetime)"
	") ENGINE=InnoDB")
TABLES['realtime_AAPL'] = (
	"CREATE TABLE `realtime_AAPL` ("
	"  `stock_name` Character(100) NOT NULL,"
	"  `datetime` datetime NOT NULL,"
	"  `open` Double NOT NULL,"
	"  `high` Double NOT NULL,"
	"  `low` Double NOT NULL,"
	"  `close` Double NOT NULL,"
	"  `volume` Double NOT NULL,"
	"  PRIMARY KEY (datetime)"
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
