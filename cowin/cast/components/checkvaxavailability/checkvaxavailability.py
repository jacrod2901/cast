from googleapiclient.http import MediaUploadProgress
import pandas as pd
from datetime import date, datetime
import time
from queue import Queue
import os
import queue
import sys




from pandas._config.config import option_context
from pandas.core.base import NoNewAttributesMixin


class CheckVaxAvailabilty:
    def __init__(self, contextvar):
        self.__componentconfig = contextvar['componentconfig']
        self.__coreconfig = contextvar['coreconfig']
        self.querygenerator = contextvar['querygenerator']
        self.makeapicall = contextvar['makeapicall']
        self.dbconnect = contextvar['dbconnect']
        self.emailutil = contextvar['emailutil']
        self.__dbconnobj = contextvar['dbconnobj']
        self.__table_name = self.__componentconfig ['user-table-name']
        self.__processedDatatbl = self.__componentconfig ['processed-apidata-table-name']
        # self.__useragelimit = self.__componentconfig['age-limit']
        self.__retrieval_cols = ["dist_name", "block_name" , "available_capacity" , "available_date" , "data_process_ts", "data_fetch_ts"]
        self.__user_req_queue = Queue()
        self.__usr_req_processed = []
        self.__max_ts = None
        self.__users_appoint_df = self.__readDatafromTbl()


    def message(self,s):
        print('{}: {}'.format(threading.current_thread().name, s))

   
    def __checkOpenRequests(self):
        __query = self.querygenerator.getUserRequestQuery()
        __query = __query.replace('placeholder_dbtablename', self.__table_name)
        data = self.dbconnect.getData(__query,self.__dbconnobj)            
        return data

    def __readDatafromTbl(self):
        __query = self.querygenerator.getUnProcessedApiDataQuery()
        __query = __query.replace('placeholder_tblname', self.__processedDatatbl)
        date_today = datetime.date(datetime.now()).strftime('%d-%m-%Y')
        __where_clause = f"where is_processed is NULL"
        __query = f"{__query} {__where_clause}"
        data = self.dbconnect.getData(__query, self.__dbconnobj)
        df = pd.DataFrame(data, columns =self.__retrieval_cols)
        print(df.dtypes)
        return df

    def __updateReqStatus(self):
        __query = self.querygenerator.getUpdateReqStatusQuery()
        __dbconn = self.dbconnect
        __curObj = self.__dbconnobj.cursor()
        __query = __query.replace('placeholder_dbtblname', self.__table_name)
        __query_new = f"{__query} {tuple(self.__usr_req_processed)}"
        __curObj.execute(__query_new)
        self.__dbconnobj.commit()

    def __updateDataProcessedStatus(self):
        print(self.__max_ts)
        __query = self.querygenerator.getUpdateProcessedStatusQuery()
        __query = __query.replace('placeholder_tblname', self.__processedDatatbl)
        __query = __query.replace('placeholder_ts', str(self.__max_ts))
        __dbconn = self.dbconnect
        __curObj = self.__dbconnobj.cursor()
        __curObj.execute(__query)
        self.__dbconnobj.commit()

    def __check_availabiity(self, open_req):
        try:
            self.__max_ts = max(self.__users_appoint_df['data_process_ts'])
            dist_name, email_id = open_req[1], open_req[2]
            date_today = datetime.date(datetime.now()).strftime('%d-%m-%Y')
            df_dist = self.__users_appoint_df[(self.__users_appoint_df['dist_name'] == dist_name) & (self.__users_appoint_df['available_capacity'] > 0) & (self.__users_appoint_df['available_date'] >= pd.to_datetime(date_today).date())] 
            df_limited_fields = df_dist[['available_capacity','dist_name' ,'block_name', 'data_fetch_ts']]
            df_limited_fields = df_limited_fields.rename(columns={'data_fetch_ts': 'available_as_on'})
            if not df_limited_fields.empty:
                res = self.emailutil.send_email(email_id, df_limited_fields.to_string())
                if res['id'] != '':
                    self.__usr_req_processed.append(email_id)
        except Exception as e:
            print(e)
            
           

    def start(self):

        open_requests = self.__checkOpenRequests()
        for i in open_requests:
            self.__user_req_queue.put(i)

        while not self.__user_req_queue.empty():
            open_req = self.__user_req_queue.get()
            self.__check_availabiity(open_req)

        if len(self.__usr_req_processed) !=0:
            self.__updateDataProcessedStatus()
            # self.__updateReqStatus()

def driver(contextvar):
    checkvaxavalblty = CheckVaxAvailabilty(contextvar)
    print('>>>>>>>>>>> Component :: CheckVaxAvailabilty :: Started <<<<<<<<<<<<')
    checkvaxavalblty.start()
    print('>>>>>>>>>>> Component :: CheckVaxAvailabilty :: Complete <<<<<<<<<<<<')





            
                    



