import datetime
import json


class ProcessNewUser:
    def __init__(self, contextvar):
        self.__componentconfig = contextvar['componentconfig']
        self.__coreconfig = contextvar['coreconfig']
        self.__dist_table_name = self.__componentconfig['dist_table_name']
        self.__new_appoint_table_name = self.__componentconfig['new_appoint_table_name']
        self.__user_table_name = self.__componentconfig['user_Table_name']
        self.querygenerator = contextvar['querygenerator']
        self.makeapicall = contextvar['makeapicall']
        self.dbconnect = contextvar['dbconnect']


    def __processNewUserData(self, user_data):
        
        self.__state_name = user_data['state_name']
        self.__district_name = user_data['district_name']
        self.__state_id = self.__getStateID()['state_id']
        is_data_exists = self.__checkDistDataExists()
        if not is_data_exists:
            district_list  = self.__getDistDataForStateID()['data']
            self.__insertDistDataDistTbl(district_list)
            self.__district_id = self.__getDistIDNewRequest()[0][0]
            new_appoint_data = self.__getAppointDataNewDist(self.__district_id)
            self.__insertAppointData(new_appoint_data, self.__district_id)
        else:
            self.__district_id = self.__getDistIDNewRequest()[0][0]
            new_appoint_data = self.__getAppointDataNewDist(self.__district_id)
            self.__insertAppointData(new_appoint_data, self.__district_id)


    def __getStateID(self):
        state_id_query = self.querygenerator.getSateIDQuery()
        state_id_query = state_id_query.replace('placeholder_state_name', self.__state_name)
        data = self.dbconnect.getData(state_id_query)
        # state_id =data[0][0]
        return {'state_id':data[0][0]}

    def __checkDistDataExists(self):
        query = self.querygenerator.getDistrictIdForStateIDQuery()
        query = query.replace('placeholder_state_id', self.__state_id)
        data = self.dbconnect.getData(query)
        if len(data) == 0:
            return False 
        return True

    
    def __insertDistDataDistTbl(self, dist_data):
        __dbconn = self.dbconnect
        __dbconnObj = __dbconn.getConnObj()
        __curObj = __dbconnObj.cursor()
        __query_original = self.querygenerator.getInsertDataDistGeoTable()
        dist_list = dist_data['districts']
        for dist_dict in dist_list:
            __query = __query_original.replace('placeholder_dbtablename', self.__dist_table_name)
            __query = __query.replace('placeholder_state_id', self.__state_id)
            __query = __query.replace('placeholder_state_name', self.__state_name)
            __query = __query.replace('placeholder_district_id', str(dist_dict['district_id']))
            __query = __query.replace('placeholder_district_name', dist_dict['district_name'])
            __curObj.execute(__query)
        __dbconnObj.commit()
        __dbconnObj.close()
        


    def __getDistDataForStateID(self):
        url = self.makeapicall.getApiLink('newdistrict')
        url = url.replace('placeholder_state_id', self.__state_id )
        data = self.makeapicall.getApiData(url)
        return data

    def __getDistIDNewRequest(self):
        __query = self.querygenerator.getDistrictIdForDistrictNameQuery()
        __query = __query.replace('placeholder_district_name', self.__district_name)
        data = self.dbconnect.getData(__query)
        return data
      
    
    def __getAppointDataNewDist(self, district_id):
        url_original = self.makeapicall.getApiLink('newappointment')
        url = url_original.replace('placeholder_district_id', district_id)
        url = url.replace('placeholder_api_hit_date', str(datetime.datetime.now().date().strftime("%d-%m-%Y")))
        data = self.makeapicall.getApiData(url)
        return data

    def __insertAppointData(self,data, district_id):
        __dbconn = self.dbconnect
        __dbconnObj = __dbconn.getConnObj()
        __curObj = __dbconnObj.cursor()
        json_data = json.dumps(data['data'])
        __query_original = self.querygenerator.getInsertDataHitsTblQuery()
        __query = __query_original.replace('placeholder_dbtablename', self.__new_appoint_table_name)
        __query = __query.replace('placeholder_status_code', str(data['status_code']))
        __query = __query.replace('placeholder_apidata', json_data)
        __query = __query.replace('placeholder_status_desc', 'NA')
        __query = __query.replace('placeholder_apits', str(datetime.datetime.now()))
        __query = __query.replace('placeholder_district_id', district_id)
        print(__query)

        __curObj.execute(__query)
        __dbconnObj.commit()
        __dbconnObj.close()


    def getNewRequests(self):
        __query = self.querygenerator.getUserRequestQuery()
        __query = __query.replace('placeholder_dbtablename', self.__user_table_name)
        data = self.dbconnect.getData(__query)
        for user_request_tup in data:
            user_req_dict = {}
            user_req_dict['state_name'] = user_request_tup[0]
            user_req_dict['district_name'] = user_request_tup[1]
            user_req_dict['email_id'] = user_request_tup[2]
            print(user_req_dict)
            self.__processNewUserData(user_data = user_req_dict)




def driver(contextvar):
    print('>>>>>>>>>>> Component :: Process New User Request :: Started <<<<<<<<<<<<')
    newReqObj = ProcessNewUser(contextvar)
    newReqObj.getNewRequests()
    print('>>>>>>>>>>> Component :: Process New User Request :: Complete <<<<<<<<<<<<')







        







