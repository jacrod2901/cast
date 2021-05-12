
class QueryGenerator:
    def __init__(self):
        # TO get All districtNames From cast_userrequests_tbl where req_status = 0.
        self.__userRequestQuery = 'SELECT state_name, district_name, email_id FROM placeholder_dbtablename where req_status is NULL'


        # TO get state_id  from cast_geo_state_tbl for input state_name.
        self.__stateIDQuery = "SELECT state_id FROM cast_geo_state_tbl WHERE state_name = 'placeholder_state_name'"


        # TO get district_id  from cast_geo_dist_tbl for input district_name.
        self.__districtIdForDistrictNameQuery = "select district_id from cast_geo_dist_tbl where district_name = 'placeholder_district_name'"


        # TO get district_id  from cast_geo_dist_tbl for input state_id
        self.__districtIdForStateIDQuery = "select district_id from cast_geo_dist_tbl where state_id = 'placeholder_state_id'"




        # Insert API HIT data in cast_hits_tbl
        self.__insertDataHitsTblQuery = """INSERT INTO placeholder_dbtablename 
                                            (status_code,status_desc,apidata, apits) 
                                            VALUES (placeholder_status_code, 'placeholder_status_desc', 'placeholder_apidata', 'placeholder_apits');"""


        # Insert New User Request Data in cast_userrequests_tbl
        self.__insertDataUserRequestTblQuery = """INSERT INTO placeholder_dbtablename 
                                                    (state_name, district_name,email_id, req_TS)
                                                    VALUES ('placeholder_state_name', 'placeholder_district_name', 'placeholder_email_id','placeholder_req_TS');"""


        # Insert New District Data in cast_geo_dist_tbl
        self.__insertDataDistGeoTableQuery = """INSERT INTO placeholder_dbtablename 
                                                    (district_id,state_id,district_name, state_name) 
                                                    VALUES ('placeholder_district_id', 'placeholder_state_id', 'placeholder_district_name', 'placeholder_state_name');"""


        # Insert New State Data in cast_geo_dist_tbl
        self.__insertDatastateGeoTableQuery = """INSERT INTO placeholder_dbtablename 
                                                    (state_id, state_name) 
                                                    VALUES ('placeholder_state_id','placeholder_state_name');"""

    def getSateIDQuery(self):
        return self.__stateIDQuery

    def getUserRequestQuery(self):
        return self.__userRequestQuery

    def getDistrictIdForDistrictNameQuery(self):
        return self.__districtIdForDistrictNameQuery

    def getDistrictIdForStateIDQuery(self):
        return self.__districtIdForStateIDQuery


    def getInsertDataHitsTblQuery(self):
        return self.__insertDataHitsTblQuery

    def getInsertDataUserRequestTblQuery(self):
        return self.__insertDataUserRequestTblQuery

    def getInsertDataDistGeoTable(self):
        return self.__insertDataDistGeoTableQuery

    def getinsertDatastateGeoTableQuery(self):
        return self.__insertDatastateGeoTableQuery


    

    
    




    
    