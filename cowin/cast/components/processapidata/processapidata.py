
from operator import index
from numpy.core.shape_base import block
import pandas as pd, datetime, os

class ProcessApiData:
    def __init__(self, contextvar):
        self.__componentconfig = contextvar['componentconfig']
        self.__coreconfig = contextvar['coreconfig']
        self.__hits_tbl = self.__componentconfig['hits_table_name']
        self.__relativecsvpath = self.__componentconfig['csv_file_path']
        self.querygenerator = contextvar['querygenerator']
        self.makeapicall = contextvar['makeapicall']
        self.dbconnect = contextvar['dbconnect']


    def __getNewData(self):
        __query = self.querygenerator.getApiHitsQuery()
        __query = __query.replace('placeholder_dbtablename', self.__hits_tbl)
        data = self.dbconnect.getData(__query)
        return data


    def __processData(self):
        data  = self.__getNewData()
        df_complete = pd.DataFrame()
        for data_tup in data:
            api_ts = data_tup[1]
            apidata = data_tup[0]
            district_id = data_tup[2]
            centers_list = apidata['centers']
            dist_name = apidata['centers'][0]['district_name']
            for data_dict in centers_list:
                # dist_name = data_dict['district_name']
                block_name = data_dict['name']
                available_sessions = data_dict['sessions']
                df_aval_sessions = pd.DataFrame(available_sessions)
                df_aval_sessions['block_name'] = block_name
                df_complete = df_complete.append(df_aval_sessions, ignore_index=True)

            df_complete['dist_name'] = dist_name
            df_complete['data_fetch_ts'] = api_ts
            df_complete['data_fetch_date'] = datetime.datetime.now().date().strftime("%d-%m-%Y")
            df_complete['district_id'] = district_id
            df_complete['data_process_ts'] = datetime.datetime.now()

        return df_complete

    def writeDFToCsv(self):
        dataDF = self.__processData()
        basepath = os.getcwd()
        __completecsvpath = f'{basepath}/{self.__relativecsvpath}'
        dataDF.to_csv(__completecsvpath, index=False, encoding='utf-8', mode='a')
        return 1 


def driver(contextvar):
    processapidata = ProcessApiData(contextvar)
    print('>>>>>>>>>>> Component :: processapidata :: Started <<<<<<<<<<<<')
    processapidata.writeDFToCsv()
    print('>>>>>>>>>>> Component :: processapidata :: Complete <<<<<<<<<<<<')











            



