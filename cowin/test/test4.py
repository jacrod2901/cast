import json
import psycopg2
from  datetime import datetime

d = {'id':1, 'data': {'centerID': 1234, 'state_name':'UttarPradesh'}}
json_data = json.dumps((d))

db_name = 'castdb'
user = 'jacrod2901'
password = 'Big@data10'
host = '127.0.0.1'
port = '5432'
table_name = "cast_hits_tbl"

con = psycopg2.connect(database = db_name, \
                        user = user,\
                        password = password,\
                        host = host,\
                        port = port)


email = 'jaitssat@gmail.com'
apnmt_date = datetime.now()
is_apnmt_available = True
no_of_apnmt = 10
# apnmt_Date_formatted = datetime.fromtimestamp(apnmt_date).strftime('%Y-%m-%d')


cur = con.cursor()
tup = (200)

sql_string = f"INSERT INTO {table_name} (status_code,status_desc,apidata, apits) VALUES (200, 'OK', '{json_data}', '{apnmt_date}');"
sql_string2 = f'''SELECT * from {table_name} where status_code in ({tup})'''
# cur.execute(sql_string);
cur.execute(sql_string2)
rows = cur.fetchall()
print(rows)


con.commit()
con.close()
