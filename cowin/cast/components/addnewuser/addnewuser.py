import datetime
class AddNewUser:
    def __init__(self, contextvar):
        self.__componentconfig = contextvar['componentconfig']
        self.__coreconfig = contextvar['coreconfig']
        self.__table_name = self.__componentconfig['user-table-name']
        self.__district_name = self.__componentconfig['district-name']
        self.__email_id = self.__componentconfig['email-id']
        self.__state_name = self.__componentconfig['state-name']
        self.__send_notification = self.__componentconfig['send-notification']
        self.__age_group = self.__componentconfig['age-group']
        self.__dbconnobj = contextvar['dbconnobj']

        self.querygenerator = contextvar['querygenerator']
        self.makeapicall = contextvar['makeapicall']
        self.dbconnect = contextvar['dbconnect']


    def loaddata(self):
        __dbconn = self.dbconnect
        __query_string = self.querygenerator.getInsertDataUserRequestTblQuery()
        __query_string = __query_string.replace('placeholder_dbtablename', self.__table_name)
        # __query_string = __query_string.replace('placeholder_state_name', self.__state_name)
        # __query_string = __query_string.replace('placeholder_district_name', self.__district_name)
        # __query_string = __query_string.replace('placeholder_email_id', self.__email_id)
        # __query_string = __query_string.replace('placeholder_req_status', )
        # __query_string = __query_string.replace('placeholder_req_TS', str(datetime.datetime.now()))
        ts = str(datetime.datetime.now())
        data_tup = (self.__state_name, self.__district_name, self.__email_id,ts, self.__send_notification, self.__age_group)
        __curObj = self.__dbconnobj.cursor()
        __curObj.execute(__query_string, data_tup)
        self.__dbconnobj.commit()


def driver(contextvar):
    addnewuser = AddNewUser(contextvar)
    print('>>>>>>>>>>> Component :: AddNewUSer :: Started <<<<<<<<<<<<')
    addnewuser.loaddata()
    print('>>>>>>>>>>> Component :: AddNewUSer :: Complete <<<<<<<<<<<<')
        