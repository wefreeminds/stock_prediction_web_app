from __future__ import print_function
import mysql.connector
cnx = mysql.connector.connect(user='george',password='george',database='PP1_historical')
cursor = cnx.cursor()

def minimum(stock_name):
    find_minimum=("select min(close)"
                  "from (select*"
                  "from PP1_historical.historical_"+stock_name+" order by date DESC LIMIT 10) as T;")
    cursor.execute(find_minimum);
    result = cursor.fetchall()
    for i in result:
        min_value = float(i[0])
        print(min_value)
        return min_value
    cnx.commit()
    cursor.close()
    cnx.close()



