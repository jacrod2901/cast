import datetime
import json
class ApiAppointmentData:
    def __init__(self, contextvar):
        self.__componentconfig = contextvar['componentconfig']
        self.__coreconfig = contextvar['coreconfig']
        self.__hits_table_name = self.__componentconfig['hits_table_name']
        self.__userrequests_table_name = self.__componentconfig['userrequests_table_name']
        self.__geo_dist_table_name = self.__componentconfig['geo_dist_table_name']
        self.querygenerator = contextvar['querygenerator']
        self.makeapicall = contextvar['makeapicall']
        self.dbconnect = contextvar['dbconnect']
        self.__dbconnobj = contextvar['dbconnobj']





    def __getDistId(self):
        __query = self.querygenerator.getDistinctDistIDQuery()
        __query = __query.replace('placeholder_geo_dist_tblname', self.__geo_dist_table_name)
        __query = __query.replace('placeholder_userrequests_tblname', self.__userrequests_table_name)
        data = self.dbconnect.getData(__query,self.__dbconnobj)
        return data


    def __getAppointDataDistID(self, district_id):
        url_original = self.makeapicall.getApiLink('newappointment')
        url = url_original.replace('placeholder_district_id', district_id)
        url = url.replace('placeholder_api_hit_date', str(datetime.datetime.now().date().strftime("%d-%m-%Y")))
        data = self.makeapicall.getApiData(url)
        return data


    def __insertAppointData(self,data, district_id):
        __dbconn = self.dbconnect
        __curObj = self.__dbconnobj.cursor()
        json_data = json.dumps(data['data'])
        __query_original = self.querygenerator.getInsertDataHitsTblQuery()
        __query = __query_original.replace('placeholder_dbtablename', self.__hits_table_name)
        __query = __query.replace('placeholder_status_code', str(data['status_code']))
        __query = __query.replace('placeholder_apidata', json_data)
        __query = __query.replace('placeholder_status_desc', 'NA')
        __query = __query.replace('placeholder_apits', str(datetime.datetime.now()))
        __query = __query.replace('placeholder_district_id', district_id)
        __curObj.execute(__query)
        self.__dbconnobj.commit()


    def insertAppntData(self):
        distid_list = self.__getDistId()
        print(f'Getting District Data for {len(distid_list)} No of District IDs ')
        if len(distid_list) ==0:
            return 0
        for idtup in distid_list:
            district_id = idtup[0]
            appnt_data = self.__getAppointDataDistID(district_id)
            self.__insertAppointData(appnt_data, district_id)
        return 1

def driver(contextvar):
    print('>>>>>>>>>>> Component :: ApiAppointmentData Request :: Started <<<<<<<<<<<<')
    newReqObj = ApiAppointmentData(contextvar)
    newReqObj.insertAppntData()
    print('>>>>>>>>>>> Component :: ApiAppointmentData Request :: Complete <<<<<<<<<<<<')


        



    

