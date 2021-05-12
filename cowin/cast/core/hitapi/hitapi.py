import requests
import json
import datetime

class MakeApiCall:
    def __init__(self):
        self.__apiHeader = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


    def __apiLink(self, category):
        link = ''
        if category.lower() == 'newstate':
            link = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/placeholder_state_id'

        if category.lower() == 'newdistrict':
            link = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/placeholder_state_id"


        if category.lower() == 'newappointment':
            link = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=placeholder_district_id&date=placeholder_api_hit_date"
 
        if category.lower() == 'allstates':
            link = "https://cdn-api.co-vin.in/api/v2/admin/location/states"

        return link

    def __apiHeader(self):
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        return header

    def getApiLink(self,category):
        return self.__apiLink(category)

    # def getApiHeader(self):
    #     return self.__apiHeader()

    def __getRequestDistrictData(self, category, district_id, api_hit_date):
        apilink = self.__apiLink(category)
        apilink = apilink.replace('placeholder_district_id', district_id)
        apilink = apilink.replace('placeholder_api_hit_date', api_hit_date)
        apiheader=self.__apiHeader
        reqObj = requests.get(apilink, headers=apiheader)
        status_code = reqObj.status_code
        data = reqObj.json()
        ts = datetime.datetime.now()

        data_dict = {'status_code':status_code, 'status_desc':'NA', 'apidata': data, 'apits':ts }
        return json.dumps(data_dict)

    def __getRequestDistrictID(self, category, state_id):
        apilink = self.__apiLink(category)
        apilink = apilink.replace('placeholder_state_id', state_id)
        apiheader=self.__apiHeader
        reqObj = requests.get(apilink, headers=apiheader)
        status_code = reqObj.status_code
        data = reqObj.json()
        return data


    def getAPiDistData(self, category,district_id,api_hit_date):
        return self.__getRequestDistrictData(category,district_id,api_hit_date)

    def getAPiDistID(self, category, state_id):
        return self.__getRequestDistrictID(category,state_id)


    def __hitapi(self, url):
        __reqObj = requests.get(url, headers=self.__apiHeader)
        __status_code = __reqObj.status_code
        __data = __reqObj.json()
        return {'status_code': __status_code, 'status_desc':'NA', 'data':__data}  

    def getApiData(self, url):
        return self.__hitapi(url)







