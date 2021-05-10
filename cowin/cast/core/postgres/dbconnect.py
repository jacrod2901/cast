import psycopg2
from  datetime import datetime
from cast.core.sqlquerygenerator.query_generator import QueryGenerator

db_name = 'testdb1'
user = 'jacrod2901'
password = 'Big@data08'
host = '127.0.0.1'
port = '5432'
table_name = "apnmt_history"

class DbConnect:
    def __init__(self, db_params):
        self.__db_params = db_params


    def __establishConn(self):
        dbname = self.__db_params['dbname']
        dbuser = self.__db_params['dbuser']
        dbpass = self.__db_params['dbpass']
        dbhost = self.__db_params['dbhost']
        dbport = self.__db_params['dbport']
        
        dbConnObj = psycopg2.connect(database = dbname, \
                        user = dbuser,\
                        password = dbpass,\
                        host = dbhost,\
                        port = dbport)

        
        return dbConnObj

    def __fetchData(self, dbtablename, query_string):
        self.__dbConnObj = self.__establishConn()
        if self.__dbConnObj.status == 1:
            curObj = dbConnObj.cursor()
            curObj.execute(query_string)
            rows = curObj.fetchall()
            self.__dbConnObj.commit()
            self.__dbConnObj.close()
            return rows

        self.__dbConnObj.commit()
        self.__dbConnObj.close()
        return []

    def getData(self, dbtablename, query_string):
        return self.__fetchData(dbtablename, query_string)

    
    def __insertDataHitsTbl(self, dbtablename, json_data):
        self.__dbConnObj = self.__establishConn()
        status_code = json_data['status_code']
        status_desc = json_data['status_desc']
        apidata = json_data['apidata']
        apits = json_Data['apits']
        __hits_sql_string = f"INSERT INTO {dbtablename} (status_code,status_desc,apidata, apits) VALUES ({status_code}, '{status_desc}', '{apidata}', '{apits}');"
        __curObj = dbConnObj.cursor()
        __curObj.execute(hits_sql_string)
        self.__dbConnObj.commit()
        self.__dbConnObj.close()

    def __insertDataUserRequestTbl(self, dbtablename, json_Data):
        self.__dbConnObj = self.__establishConn()
        district_name = json_data['district_name']
        email_id = json_data['email_id']
        req_status = json_data[' req_status']
        req_date= json_Data['req_date']
        __userreq_sql_string = f"INSERT INTO {dbtablename} (district_name,email_id,req_status, req_date) VALUES ({district_name}, '{email_id}', '{req_status}', '{req_date}');"
        __curObj = dbConnObj.cursor()
        __curObj.execute(hits_sql_string)
        self.__dbConnObj.commit()
        self.__dbConnObj.close()

    def ingestDataUserRequest(self, dbtablename, json_Data):
        self.__insertDataUserRequestTbl(dbtablename, json_Data)

    def ingestDataHitsTbl(self, dbtablename, json_Data):
        self.__insertDataHitsTbl(dbtablename, json_data)




    





    








                    


