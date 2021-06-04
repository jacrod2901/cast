
from operator import index
from numpy.core.shape_base import block
import pandas as pd, datetime, os

class ProcessApiData:
    def __init__(self, contextvar):
        self.__componentconfig = contextvar['componentconfig']
        self.__jsonconfig = contextvar['jsonconfig']
        self.__coreconfig = contextvar['coreconfig']
        self.__hits_tbl = self.__componentconfig['hits_table_name']
        self.__processedapidatatbl = self.__componentconfig['processedapidata_table_name']
        self.querygenerator = contextvar['querygenerator']
        self.makeapicall = contextvar['makeapicall']
        self.dbconnect = contextvar['dbconnect']
        self.__dbconnobj = contextvar['dbconnobj']
        self.__max_data_process_ts = None


    def __getNewData(self):
        last_apidata_ts = self.__jsonconfig.getJsonData()['last-apidata-timestamp']
        __query = self.querygenerator.getApiHitsQuery()
        __query = __query.replace('placeholder_dbtablename', self.__hits_tbl)
        __where_clause = f" and apits > '{last_apidata_ts}'"
        __query_complete = f"{__query} {__where_clause}"
        data = self.dbconnect.getData(__query_complete,self.__dbconnobj)
        return data


    def processData(self):
        data  = self.__getNewData()
        print(f'Processing  {len(data)} No of API Data' )
        df_complete = pd.DataFrame()
        
        for data_tup in data:
            api_ts = data_tup[1]
            apidata = data_tup[0]
            district_id = data_tup[2]
            centers_list = apidata['centers']
            dist_name = apidata['centers'][0]['district_name']
            data_fetch_dt = datetime.datetime.now().date().strftime("%d-%m-%Y")
            data_process_ts = datetime.datetime.now()
            self.__max_data_process_ts = str(api_ts)
            is_processed = None
            for data_dict in centers_list:
                # dist_name = data_dict['district_name']
                block_name = data_dict['name']
                available_sessions = data_dict['sessions']
                for sessions_dict in data_dict['sessions']:
                    session_tup = (sessions_dict['session_id'],sessions_dict['date'],sessions_dict['available_capacity'],sessions_dict['min_age_limit'],sessions_dict['vaccine'],sessions_dict['available_capacity_dose1'],sessions_dict['available_capacity_dose2'],data_dict['name'], dist_name, api_ts, data_fetch_dt, district_id, data_process_ts )
                    self.writeProcessedDatatoDB(session_tup)
                    self.__jsonconfig.updateDocumentTS(self.__max_data_process_ts) #Update Document TS
        return 1

    def writeProcessedDatatoDB(self, data):
        __dbconn = self.dbconnect
        __curObj = self.__dbconnobj.cursor()
        __query = self.querygenerator.getInsertProcessedApiDataQuery()
        __query = __query.replace('placeholder_dbtblname', self.__processedapidatatbl)
        __curObj.execute(__query, data)
        self.__dbconnobj.commit()
        

    

def driver(contextvar):
    processapidata = ProcessApiData(contextvar)
    print('>>>>>>>>>>> Component :: processapidata :: Started <<<<<<<<<<<<')
    processapidata.processData()
    print('>>>>>>>>>>> Component :: processapidata :: Complete <<<<<<<<<<<<')











            



