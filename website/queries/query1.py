from __future__ import print_function
import mysql.connector
cnx = mysql.connector.connect(user='root',password='Anilraji95*',database='pp1_real_time')
cursor = cnx.cursor()

def current(stock_name):
    find_average=("select close "
                  "from (select*"
                  "from pp1_historical.historical_"+stock_name+" order by date DESC LIMIT 1)as T;")
    cursor.execute(find_average);
    result = cursor.fetchall()
    for i in result:
        current_val= float(i[0])
        print("aapl {}".format(current_val))
        return current_val
    cnx.commit()
    cursor.close()
    cnx.close()
