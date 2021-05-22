
class LoadStateData:
    def __init__(self, contextvar):
        self.__componentconfig = contextvar['componentconfig']
        self.__coreconfig = contextvar['coreconfig']
        self.__table_name = self.__componentconfig['state_table_name']
        self.querygenerator = contextvar['querygenerator']
        self.makeapicall = contextvar['makeapicall']
        self.dbconnect = contextvar['dbconnect']


    def __getstateDataFromApi(self):
        apilink = self.makeapicall.getApiLink('allstates')
        apidata = self.makeapicall.getApiData(apilink)
        return apidata['data']

    
    def loaddata(self):
        state_list = self.__getstateDataFromApi()['states']
        __query_string_original = self.querygenerator.getinsertDatastateGeoTableQuery()
        # __query_string = __query_string_original.replace('placeholder_dbtablename', self.__table_name)
        __dbconn = self.dbconnect
        __dbconnObj = __dbconn.getConnObj()
        __curObj = __dbconnObj.cursor()
        
        for state_dict in state_list:
            state_id = str(state_dict['state_id'])
            state_name = (state_dict['state_name'])
            __query_string = __query_string_original.replace('placeholder_dbtablename', self.__table_name)
            __query_string = __query_string.replace('placeholder_state_id', state_id)
            __query_string = __query_string.replace('placeholder_state_name', state_name)
            __curObj.execute(__query_string)
        __dbconnObj.commit()
        __dbconnObj.close()
        


def driver(contextvar):
    loadstatedata = LoadStateData(contextvar)
    print('>>>>>>>>>>> Component :: LoadStateData :: Started <<<<<<<<<<<<')
    loadstatedata.loaddata()
    print('>>>>>>>>>>> Component :: LoadStateData :: Complete <<<<<<<<<<<<')






  



