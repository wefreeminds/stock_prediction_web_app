from __future__ import print_function
import requests
import datetime as DT
import time
import csv
import mysql.connector
cnx = mysql.connector.connect(user='root',password='Anilraji95*',database='pp1_real_time')
cursor = cnx.cursor()

stock_names =['AMZN', 'PETX', 'AABA', 'AAPL', 'NVDA','TXN', 'NDAQ', 'GOOG', 'FB', 'GS']
for stock_name in stock_names:
	#print(stock_name)
	find_min=("select min(close)"
		"from (select* "
		"from pp1_historical.historical_"+stock_name+" order by date DESC LIMIT 10)as T;")
	cursor.execute(find_min);
	result = cursor.fetchall()
	for i in result:
		minimum= float(i[0])
		print("minimum= {}".format(minimum))

	find_average=("select avg(close)"
		"from (select*"
		"from pp1_historical.historical_"+stock_name+" order by date DESC LIMIT 10)as T;")
	cursor.execute(find_average);
	result = cursor.fetchall()
	for i in result:
		average= float(i[0])
		print("average={}".format(average))

	if(minimum < average):
		print(stock_name+"has its minimum value less that the average value")

	if(minimum> average):
		print(stock_name+"minimum higher than the average")

cnx.commit()
cursor.close()
cnx.close()