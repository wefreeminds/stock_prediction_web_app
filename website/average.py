from __future__ import print_function
import mysql.connector
cnx = mysql.connector.connect(user='george',password='george',database='PP1_historical')
cursor = cnx.cursor()
def average(stock_name):
    find_average=("select avg(close)"
                  "from (select*"
                  "from PP1_historical.historical_"+stock_name+" order by date DESC LIMIT 100) as T;")
    cursor.execute(find_average);
    result = cursor.fetchall()
    for i in result:
        average_value = float(i[0])
        print(average_value)
        return average_value
    cnx.commit()
    cursor.close()
    cnx.close()


