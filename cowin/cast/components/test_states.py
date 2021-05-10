import requests
import json


import requests
import json


header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
link = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/34"
f = requests.get(link, headers=header)
# url="https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP"

# myobj = {'mobile': '9740904367'}
# x = requests.post(url, json = myobj, headers=header)

if f.status_code != 200:
  print ("Error:", x.status_code)

d =  f.json()
print(d)
# for i in range(len(d['centers'])):
#   state = d['centers'][i]['state_name']
#   district = d['centers'][i]['district_name']
#   block_name = d['centers'][i]['block_name']
#   print(state, district, block_name)
