import requests
import json


import requests
import json


header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=637&date=08-05-2021"
link2 = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
link3 = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/16"
f = requests.get(link, headers=header)
# url="https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP"

# myobj = {'mobile': '9740904367'}
# x = requests.post(url, json = myobj, headers=header)

# if f.status_code != 200:
#   print ("Error:", x.status_code)

d =  f.json()
print(d)
# states = d['states']
# for state_dict in states:
#   print(state_dict)
# print(len(d['centers']))
# for i in range(len(d['centers'])):
#   state = d['centers'][i]['state_name']
#   district = d['centers'][i]['district_name']
#   block_name = d['centers'][i]['block_name']
#   sessions = d['centers'][i]['sessions']
#   print(state, district, block_name, len(sessions))


# {'session_id': '824a9e3d-09d8-43cc-a52e-384c75ed3413', 'date': '08-05-2021', 'available_capacity': 120, 'min_age_limit': 45, 'vaccine': 'COVISHIELD', 'slots': ['09:00AM-11:00AM', '11:00AM-01:00PM', '01:00PM-03:00PM', '03:00PM-05:00PM']}
# {'session_id': '2dad52a0-92e4-47f8-9f35-9fc87341ed3d', 'date': '10-05-2021', 'available_capacity': 120, 'min_age_limit': 45, 'vaccine': 'COVISHIELD', 'slots': ['09:00AM-11:00AM', '11:00AM-01:00PM', '01:00PM-03:00PM', '03:00PM-05:00PM']}
# {'session_id': '36fc87b7-b2b4-45af-8b8e-e331fe05b596', 'date': '11-05-2021', 'available_capacity': 120, 'min_age_limit': 45, 'vaccine': 'COVISHIELD', 'slots': ['09:00AM-11:00AM', '11:00AM-01:00PM', '01:00PM-03:00PM', '03:00PM-05:00PM']}
# {'session_id': 'bdc0d513-3213-41a7-bfcc-7f1192f88f51', 'date': '12-05-2021', 'available_capacity': 120, 'min_age_limit': 45, 'vaccine': 'COVISHIELD', 'slots': ['09:00AM-11:00AM', '11:00AM-01:00PM', '01:00PM-03:00PM', '03:00PM-05:00PM']}
# {'session_id': '1eb0ba53-8de1-40dd-aff6-8c4278dea4d9', 'date': '13-05-2021', 'available_capacity': 120, 'min_age_limit': 45, 'vaccine': 'COVISHIELD', 'slots': ['09:00AM-11:00AM', '11:00AM-01:00PM', '01:00PM-03:00PM', '03:00PM-05:00PM']}
# {'session_id': '698a7ed3-ba72-4369-9572-1ae8871e40da', 'date': '14-05-2021', 'available_capacity': 120, 'min_age_limit': 45, 'vaccine': 'COVISHIELD', 'slots': ['09:00AM-11:00AM', '11:00AM-01:00PM', '01:00PM-03:00PM', '03:00PM-05:00PM']}