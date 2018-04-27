from __future__ import print_function
import mysql.connector
cnx = mysql.connector.connect(user='george',password='george',database='PP1_real_time')
cursor = cnx.cursor()

def current(stock_name):
    find_average=("select close "
                  "from (select *"
                  "from PP1_real_time.realtime_"+stock_name+" order by datetime DESC LIMIT 1) as T;")
    cursor.execute(find_average)
    result = cursor.fetchall()
    for i in result:
        current_val= float(i[0])
        print("aapl {}".format(current_val))
        return current_val
    cnx.commit()
    cursor.close()
    cnx.close()


