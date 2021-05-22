import pandas as pd

df = pd.read_csv('resources/output.csv')
df_filtered_18 = df[(df['date'] >= df['data_fetch_date']) & (df['available_capacity'] > 0) & (df['min_age_limit'] == 18)]
df_filtered_45 = df[(df['date'] >= df['data_fetch_date']) & (df['available_capacity'] > 0) & (df['min_age_limit'] == 45)]

dist_id = df_filtered_18['district_id'].drop_duplicates().tolist()
print(dist_id)

df_filtered_18 = df_filtered_18.rename({'data_fetch_ts': 'available_as_on'}, axis=1)
df_filtered_45 = df_filtered_45.rename({'data_fetch_ts': 'available_as_on'}, axis=1)
# print(df_filtered_18.columns)

# Prepare Data
print(df_filtered_18[['available_capacity', 'min_age_limit','block_name','available_as_on','district_id']])

print(df_filtered_45[['vaccine','available_capacity', 'min_age_limit','block_name','available_as_on','district_id']])
import pywhatkit

