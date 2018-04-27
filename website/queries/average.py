from __future__ import print_function
import requests
import datetime as DT
import time
import csv
import mysql.connector
cnx = mysql.connector.connect(user='george',password='george',database='pp1_real_time')
cursor = cnx.cursor()

#stock_names =['AMZN', 'PETX', 'AABA', 'AAPL', 'NVDA','TXN', 'NDAQ', 'GOOG', 'FB', 'GS']
#for stock_name in stock_names:
	#print(stock_name)
find_average=("select avg(close)"
	"from (select*"
	"from pp1_historical.historical_aapl order by date DESC LIMIT 10)as T;")
cursor.execute(find_average);
result = cursor.fetchall()
for i in result:
    maximum= float(i[0])
    print(maximum)
cnx.commit()
cursor.close()
cnx.close()
