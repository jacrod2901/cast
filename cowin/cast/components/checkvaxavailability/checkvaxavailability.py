from googleapiclient.http import MediaUploadProgress
import pandas as pd
from datetime import date, datetime
import time
from queue import Queue
import threading
import os
from functools import partial
from multiprocessing.pool import Pool
import queue
import multiprocessing
from multiprocessing import Process
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
        self.__table_name = self.__componentconfig ['user-table-name']
        self.__processedDatatbl = self.__componentconfig ['processed-apidata-table-name']
        self.__csvpath = self.__componentconfig ['output-csv-path']
        # self.__useragelimit = self.__componentconfig['age-limit']
        self.__retrieval_cols = ["dist_name", "block_name" , "available_capacity" , "available_date" , "data_fetch_ts"]
        self.__user_req_queue = Queue()
        self.__num_threads = multiprocessing.cpu_count()-2
        self.__usr_req_processed = []
        self.__max_ts = None
        self.__users_appoint_df = self.__readDatafromTbl()


    def message(self,s):
        print('{}: {}'.format(threading.current_thread().name, s))

    def do_job(self,tasks_to_accomplish, tasks_that_are_done, data):
        while True:
            print('Doing Job')
            try:
                '''
                    try to get task from the queue. get_nowait() function will 
                    raise queue.Empty exception if the queue is empty. 
                    queue(False) function would do the same task also.
                '''
                open_req = tasks_to_accomplish.get_nowait()
                self.__check_availabiity(open_req, data)
            except queue.Empty:

                break
            else:
                '''
                    if no exception has been raised, add the task completion 
                    message to task_that_are_done queue
                '''
                # print(open_req)
                tasks_that_are_done.put(open_req)
                time.sleep(.5)
        return True

    def __checkOpenRequests(self):
        __query = self.querygenerator.getUserRequestQuery()
        __query = __query.replace('placeholder_dbtablename', self.__table_name)
        data = self.dbconnect.getData(__query)            
        return data

    def __readDatafromTbl(self):
        __query = self.querygenerator.getUnProcessedApiDataQuery()
        __query = __query.replace('placeholder_tblname', self.__processedDatatbl)
        date_today = datetime.date(datetime.now()).strftime('%d-%m-%Y')
        __where_clause = f"where is_processed is NULL and available_capacity > 0 and available_date >= '{date_today}'"
        __query = f"{__query} {__where_clause}"
        data = self.dbconnect.getData(__query)
        df = pd.DataFrame(data, columns =self.__retrieval_cols)
        return df

    def __updateReqStatus(self):
        __query = self.querygenerator.getUpdateReqStatusQuery()
        __dbconn = self.dbconnect
        __dbconnObj = __dbconn.getConnObj()
        __curObj = __dbconnObj.cursor()
        __query = __query.replace('placeholder_dbtblname', self.__table_name)
        __query_new = f"{__query} {tuple(self.__usr_req_processed)}"
        __curObj.execute(__query_new)
        __dbconnObj.commit()
        __dbconnObj.close()

    def __updateDataProcessedStatus(self):
        __query = self.querygenerator.getUpdateProcessedStatusQuery()
        __query = __query.replace('placeholder_tblname', self.__processedDatatbl)
        __query = __query.replace('placeholder_ts', str(self.__max_ts))
        __dbconn = self.dbconnect
        __dbconnObj = __dbconn.getConnObj()
        __curObj = __dbconnObj.cursor()
        __curObj.execute(__query)
        __dbconnObj.commit()
        __dbconnObj.close()

    def __check_availabiity(self, open_req):
        try:
            self.__max_ts = max(self.__users_appoint_df['data_fetch_ts'])
            dist_name, email_id = open_req[1], open_req[2]
            df_dist = self.__users_appoint_df[(self.__users_appoint_df['dist_name'] == dist_name) ]#& (users_appoint_df['available_capacity'] > 0) & (users_appoint_df['available_date'] >= date_today)] 
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
        # with Pool(self.__num_threads) as p:
        #     p.map(self.__check_availabiity, open_requests)

        for i in open_requests:
            self.__user_req_queue.put(i)

        while not self.__user_req_queue.empty():
            open_req = self.__user_req_queue.get()
            self.__check_availabiity(open_req)

        if len(self.__usr_req_processed) !=0:
            self.__updateDataProcessedStatus()
            # self.__updateReqStatus()


        # for open_req in number_of_task:
        #         tasks_to_accomplish.put(open_req)
        # print(tasks_to_accomplish)
        # # creating processes
        # for w in range(number_of_processes):
        #     p = Process(target=self.do_job, args=(tasks_to_accomplish, tasks_that_are_done, users_appoint_df))
        #     processes.append(p)
        #     p.start()

        # completing process
        # for p in processes:
        #     p.join()       
        
        #  # print the output
        # while not tasks_that_are_done.empty():
        #     print(tasks_that_are_done.get())

        # return True


        # if len(open_requests) ==0:
        #     return 0
        # for open_req in open_requests:
        #     self.__user_req_queue.put(open_req)

        # users_appoint_df = self.__readDatafromTbl()
        # for i in range(self.__num_threads):
        #     worker = threading.Thread(target=self.__check_availabiity, args=(self.__user_req_queue,users_appoint_df), name='WORKER-{}'.format(i))
        #     worker.setDaemon(True)
        #     worker.start()
        # # self.message('*** Main Thread Waiting')
        # self.__user_req_queue.join()
        # # self.message('*** Done')
        # if not len(self.__usr_req_processed) ==0:
        #     self.__updateReqStatus()
        # if self.__max_ts:
        #     self.__updateDataProcessedStatus()

def driver(contextvar):
    checkvaxavalblty = CheckVaxAvailabilty(contextvar)
    print('>>>>>>>>>>> Component :: CheckVaxAvailabilty :: Started <<<<<<<<<<<<')
    checkvaxavalblty.start()
    print('>>>>>>>>>>> Component :: CheckVaxAvailabilty :: Complete <<<<<<<<<<<<')
    sys.exit()





            
                    



