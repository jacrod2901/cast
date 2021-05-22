from pandas.core import api
import psycopg2
import pandas as pd
import datetime
db_name = 'castdb'
user = 'jacrod2901'
password = 'Big@data10'
host = '127.0.0.1'
port = '5432'
table_name = "cast_usrrequests_tbl"

query_string = "select state_name, district_name, req_ts from cast_userrequests_tbl where req_status is NULL"
qs2 = "select state_id, state_name from cast_geo_state_tbl where state_name = 'Uttar Pradesh'"
qs3 = "select apidata, apits from cast_hits_tbl where status_code = 200"
qs4 = """select json_extract_path_text(apidata, 'centers')  as centers, 
 from cast_hits_tbl"""
'''json_extract_path_text (json_array_elements (json_extract_path(apidata, 'sessions')), 'session', 'abc') As session'''

dbConnObj = psycopg2.connect(database = db_name, \
                        user = user,\
                        password = password,\
                        host = host,\
                        port = port)

        
curObj = dbConnObj.cursor()
curObj.execute(qs3)
rows = curObj.fetchall()
dbConnObj.commit()
dbConnObj.close()

print(rows)
# df_complete = pd.DataFrame()
# centers_list = rows[0][0]['centers']
# print(type(centers_list))
# apits = rows[0][1]
# print(apits)
# dist_name = 'UP'
for dict in rows[0][0]['centers']:
    dist_name = dict['district_name']
    print(dist_name)
#     center = centers_dict[i]['name']
#     available_sessions = centers_dict[i]['sessions']
#     # print(available_sessions)
#     # dict = {'district_name': dist_name, 'center': center, 'session_availablity': len(available_sessions), 'session_onject':available_sessions}
#     df_sessions = pd.DataFrame(available_sessions)
#     df_sessions['blockname'] = center
#     df_complete = df_complete.append(df_sessions, ignore_index=True)
#     # print(df_complete)

# df_complete['dist_name'] = dist_name
# df_complete['data_fetch_ts'] = apits
# df_complete['data_process_ts'] = datetime.datetime.now()
# print(df_complete)
    


# # available_sessions = centers_dict[1]['sessions']

# # df = pd.DataFrame(available_sessions)
# # df_centers = pd.DataFrame(centers_dict)
# # print(df)
#     # available_sessions = []
#     # dict = {}
#     # try:
#     #     available_sessions[0]
#     #     dict = {'district_name': dist_name, 'center': center, 'session_availablity': len(available_sessions), 'session_onject':available_sessions}

#     # except:
#     #     dict = {'district_name': dist_name, 'center': center, 'session_availablity': 0, 'session_onject':available_sessions}

#     # print(dict)
    
#     # while i > 0:
#     #     aval_capacity = available_sessions[i]['available_capacity']
#     #     min_age_limit = available_sessions[i]['min_age_limit']
#     #     vaccine = available_sessions[i]['vaccine']
#     #     slots = available_sessions[i]['slots']
#     #     i+=1
