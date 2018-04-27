from __future__ import print_function
import mysql.connector
cnx = mysql.connector.connect(user='root',password='Anilraji95*',database='pp1_real_time')
cursor = cnx.cursor()
def average(stock_name):
    find_average=("select avg(close)"
                  "from (select*"
                  "from pp1_historical.historical_"+stock_name+" order by date DESC LIMIT 10)as T;")
    cursor.execute(find_average);
    result = cursor.fetchall()
    for i in result:
        average_value = float(i[0])
        print(average_value)
        return average_value
    cnx.commit()
    cursor.close()
    cnx.close()
