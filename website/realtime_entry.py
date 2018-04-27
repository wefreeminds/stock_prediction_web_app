from __future__ import print_function
APIkey='PV7KXHYLKJK9Q3YG'
import requests
import datetime as DT
import time
import csv
import mysql.connector
cnx = mysql.connector.connect(user='george',password='george', database='PP1_real_time')
cursor = cnx.cursor()
import os

stock_names =['AMZN', 'PETX', 'AABA', 'AAPL', 'NVDA','TXN', 'NDAQ', 'GOOG', 'FB', 'GS']
for stock_name in stock_names:
	print(stock_name)

	result = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+stock_name+'&interval=1min&apikey='+APIkey)
	data = result.json()["Time Series (1min)"]
	add_real = ("INSERT INTO realtime_"+stock_name+
        	   "(stock_name,datetime, open, high,low,close,volume)"
    	       "VALUES (%s, %s, %s, %s, %s,%s,%s)")
        app_dir ='/home/georgeha/web_apps_class/stock_prediction_web_app/website'
        stock_dir = os.path.join(app_dir,stock_name)
        with open(stock_dir +'.csv', 'w') as outcsv:
		fieldnames=["name","date","open","high","low","close","volume"]
		w=csv.writer(outcsv)
		w.writerow(fieldnames)
		outcsv.close()


	realtime_data=[]
	count=0
	keys=data.keys()
	keys=sorted(keys)
	keys.reverse()
	for k in keys:
		if count<1440:
			tup={}
			tup['datetime']=k
			tup['open']=data[k]['1. open']
			tup['high']=data[k]["2. high"]
			tup['low']=data[k]["3. low"]
			tup['close']=data[k]["4. close"]
			tup['volume']=data[k]["5. volume"]
			realtime_data.append(tup)
			count+=1
		else:
			break 
	cursor.execute("TRUNCATE TABLE realtime_"+stock_name)
	for r in range(len(realtime_data)):
			temp_data=stock_name,realtime_data[r]["datetime"],realtime_data[r]["open"],realtime_data[r]["high"],realtime_data[r]["low"],realtime_data[r]["close"],realtime_data[r]["volume"]
			#print(temp_data)
			with open(stock_dir + '.csv', 'a') as outcsv:
				writer = csv.writer(outcsv)
				writer.writerow(temp_data)
				#print("updating csv")
				outcsv.close()
			cursor.execute(add_real,temp_data)
cnx.commit()
cursor.close()
cnx.close()

	
