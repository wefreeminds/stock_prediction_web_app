from __future__ import print_function
APIkey='R90NK9CMU0WUOEXG'
import requests
import datetime as DT
import time
import os
import csv
import mysql.connector
cnx = mysql.connector.connect(user='george',password='george',database='PP1_historical')
cursor = cnx.cursor()


stock_names =['AMZN', 'PETX', 'AABA', 'AAPL', 'NVDA','TXN', 'NDAQ', 'GOOG', 'FB', 'GS']
for stock_name in stock_names:
	print(stock_name)
	result = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stock_name+'&outputsize=full&apikey='+APIkey)
	data = result.json()['Time Series (Daily)']
	now = DT.date.today()
	year_ago=now- DT.timedelta(days=1)


	add_history = ("INSERT INTO historical_"+stock_name+
			   "(stock_name,date, open, high,low,close,volume)"
			   "VALUES (%s, %s, %s, %s, %s,%s,%s)")
	
        app_dir ='/home/georgeha/web_apps_class/stock_prediction_web_app/website/'
        #stock_dir = os.path.join(app_dir,stock_name)
	
        with open( app_dir + 'historical_' + stock_name+ '.csv', 'w') as outcsv:
		fieldnames=["name","date","open","high","low","close","volume"]
		w=csv.writer(outcsv)
		w.writerow(fieldnames)
		outcsv.close()	

	historical_data=[]
	count=1
	while count<=365:
		year_ago = year_ago - DT.timedelta(days=1)
		
		try:
			tup={}
			tup['date']=str(year_ago)
			tup['open']=data[str(year_ago)]['1. open']
			tup['high']=data[str(year_ago)]["2. high"]
			tup['low']=data[str(year_ago)]["3. low"]
			tup['close']=data[str(year_ago)]["4. close"]
			tup['volume']=data[str(year_ago)]["5. volume"]
			historical_data.append(tup)
			count+=1
		except:
			pass
	cursor.execute("TRUNCATE TABLE historical_"+stock_name)

	for h in range(len(historical_data)):
		temp_data=stock_name,historical_data[h]["date"],historical_data[h]["open"],historical_data[h]["high"],historical_data[h]["low"],historical_data[h]["close"],historical_data[h]["volume"]
		#print(temp_data)
		with open(app_dir + 'historical_' + stock_name+ '.csv', 'a') as outcsv:
			writer = csv.writer(outcsv)
			writer.writerow(temp_data)
			#print("updating csv")
			outcsv.close()
		cursor.execute(add_history,temp_data)


cnx.commit()
cursor.close()
cnx.close()
