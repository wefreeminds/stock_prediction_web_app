from __future__ import print_function
import mysql.connector
cnx = mysql.connector.connect(user='george', password='george', database='PP1_historical')
cursor = cnx.cursor()

def maximum(stock_name):
    find_average=("select max(close)"
                  "from (select*"
                  "from PP1_historical.historical_"+stock_name+" order by date DESC LIMIT 10) as T;")
    cursor.execute(find_average)
    result = cursor.fetchall()
    for i in result:
        maximum= float(i[0])
        return maximum
    cnx.commit()
    cursor.close()
    cnx.close()



