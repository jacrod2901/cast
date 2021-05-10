import requests
import json
import datetime

class MakeApiCall:
    def __init__(self,district_id, api_hit_date):
        self.__district_id = district_id
        self.__api_hit_date = api_hit_date


    def __apiLink(self, category):
        link = ''
        if category.lower() == 'newstate':
            link = f'https://cdn-api.co-vin.in/api/v2/admin/location/districts/placeholder_state_id'

        if category.lower() == 'newdiscrict':
            link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=placeholder_district_id&date=placeholder_api_hit_date"

        return link

    def __apiHeader(self):
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        return header

    def getApiLink(self,category):
        return self.__apiLinks(category)

    def getApiHeader(self):
        return self.__apiHeader()

    def __getRequestDistrictData(self, category, district_id, api_hit_date):
        apilink = self.__apiLink(category)
        apilink = apilink.replace('placeholder_district_id', district_id)
        apilink = apilink.replace('placeholder_api_hit_date', api_hit_date)
        apiheader=vself.__apiHeader
        reqObj = requests.get(apilink, headers=apiheader)
        status_code = reqObj.status_code
        data = reqObj.json()
        ts = datetime.datetime.now()

        data_dict = {'status_code':status_code, status_desc:'NA', apidata: data, apits:ts }
        return json.dumps(data_dict)

    def __getRequestDistrictID(self, category, state_id):
        apilink = self.__apiLink(category)
        apilink = apilink.replace('placeholder_state_id', state_id)
        apiheader=vself.__apiHeader
        reqObj = requests.get(apilink, headers=apiheader)
        status_code = reqObj.status_code
        data = reqObj.json()
        return data


    def getAPiDistData(self, category,district_id,api_hit_date):
        return self.__getRequestDistrictData(category,district_id,api_hit_date)

    def getAPiDistID(self, category, state_id):
        return self.__getRequestDistrictID(category,state_id)





