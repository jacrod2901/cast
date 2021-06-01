from googleapiclient.http import MediaUploadProgress
import pandas as pd
from datetime import date, datetime
import time
from queue import Queue
import threading
import os


from pandas._config.config import option_context


class CheckVaxAvailabilty:
    def __init__(self, contextvar):
        self.__componentconfig = contextvar['componentconfig']
        self.__coreconfig = contextvar['coreconfig']
        self.__table_name = self.__componentconfig ['user-table-name']
        self.__csvpath = self.__componentconfig ['output-csv-path']
        self.querygenerator = contextvar['querygenerator']
        self.makeapicall = contextvar['makeapicall']
        self.dbconnect = contextvar['dbconnect']
        self.emailutil = contextvar['emailutil']
        self.__user_req_queue = Queue()
        self.__num_threads = os.cpu_count()-1
        self.__usr_req_processed = []


    def message(self,s):
        print('{}: {}'.format(threading.current_thread().name, s))


    def __checkOpenRequests(self):
        __query = self.querygenerator.getUserRequestQuery()
        __query = __query.replace('placeholder_dbtablename', self.__table_name)
        data = self.dbconnect.getData(__query)            
        return data

    def __readCSV(self):
        return pd.read_csv(self.__csvpath)


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


    def __checkAppointment(self):
        open_requests = self.__checkOpenRequests()
        if len(open_requests) > 0:
            date_today = datetime.date(datetime.now().strftime('%d-%m-%Y'))
            users_appoint_df = self.__readCSV()
            for open_req in open_requests:
                self.__user_req_queue.put(open_req)

                # dist_name, email_id = open_req[0], open_req[1]
                # df_dist = users_appoint_df[(users_appoint_df['dist_name'] == dist_name) & (users_appoint_df['available_capacity'] > 0) & (users_appoint_df['date'] >= date_today)] 
                # df_limited_fields = df_dist[['available_capacity', 'block_name', 'data_fetch_ts']]
                # df_limited_fields = df_limited_fields.rename(columns={'data_fetch_ts': 'available_as_on'})
                # if not df_limited_fields.empty:
    
    
    def __check_availabiity(self, q):
        while True:
            users_appoint_df = self.__readCSV()
            open_req = q.get()
            # date_today = datetime.date(datetime.now()).strftime('%d-%m-%Y')
            # date_today = datetime.date(datetime(2021, 5, 15)).strftime('%d-%m-%Y') 
            date_today = '15-05-2021'           
            dist_name, email_id = open_req[1], open_req[2]
            df_dist = users_appoint_df[(users_appoint_df['dist_name'] == dist_name) & (users_appoint_df['available_capacity'] > 0) & (users_appoint_df['date'] >= date_today)] 
            df_limited_fields = df_dist[['available_capacity', 'block_name', 'data_fetch_ts']]
            df_limited_fields = df_limited_fields.rename(columns={'data_fetch_ts': 'available_as_on'})
            if not df_limited_fields.empty:
                res = self.emailutil.send_email(email_id, df_limited_fields.to_string())
                if res['id'] != '':
                    self.__usr_req_processed.append(email_id)
            q.task_done()


    def start(self):
        open_requests = self.__checkOpenRequests()
        if len(open_requests) ==0:
            return 0
        for open_req in open_requests:
            self.__user_req_queue.put(open_req)

        for i in range(self.__num_threads):
            worker = threading.Thread(target=self.__check_availabiity, args=(self.__user_req_queue,), name='WORKER-{}'.format(i))
            worker.setDaemon(True)
            worker.start()
        # self.message('*** Main Thread Waiting')
        self.__user_req_queue.join()
        # self.message('*** Done')
        self.__updateReqStatus()

def driver(contextvar):
    checkvaxavalblty = CheckVaxAvailabilty(contextvar)
    print('>>>>>>>>>>> Component :: CheckVaxAvailabilty :: Started <<<<<<<<<<<<')
    checkvaxavalblty.start()
    print('>>>>>>>>>>> Component :: CheckVaxAvailabilty :: Complete <<<<<<<<<<<<')





            
                    



