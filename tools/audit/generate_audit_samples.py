import json
import pandas as pd
import requests

# 1. Fetch first 20 rows of Nagpur APY from UPAg / India Data Portal CKAN
url_ckan = 'https://ckandev.indiadataportal.com/api/3/action/datastore_search'
params = {
    'resource_id': '6f70d961-3a4f-4caa-b08f-f72f708791e1',
    'filters': json.dumps({'district_name': 'Nagpur'}),
    'limit': 20
}
r_ckan = requests.get(url_ckan, params=params, timeout=15)
records_ckan = r_ckan.json()['result']['records']
df_ckan = pd.DataFrame(records_ckan)[['year', 'season', 'crop_name', 'crop_category', 'area', 'production', 'yield']]
print('=== 1. UPAg APY 20 ROWS ===')
print(df_ckan.to_markdown(index=False))

# 2. Monthly Rainfall Nagpur (first 20 rows) from ICRISAT / IMD raw dataset
url_rain = 'https://raw.githubusercontent.com/amar-at-iitm/ma5755-capstone-project/main/data/raw/monthly_rainfall_data.csv'
df_rain_all = pd.read_csv(url_rain)
nagpur_rain = df_rain_all[df_rain_all['Dist Name'].str.upper() == 'NAGPUR'].sort_values('Year')
cols_rain = ['Year', 'JUNE RAINFALL (Millimeters)', 'JULY RAINFALL (Millimeters)', 'AUGUST RAINFALL (Millimeters)', 'SEPTEMBER RAINFALL (Millimeters)']
print('\n=== 2. RAINFALL 20 ROWS ===')
print(nagpur_rain[cols_rain].head(20).to_markdown(index=False))

# 3. Mandi Prices Nagpur (first 20 rows) from CMO Maharashtra
url_mandi = 'https://raw.githubusercontent.com/joshi-vipul/maharashtra_mandi/master/Monthly_data_cmo.csv'
df_mandi_all = pd.read_csv(url_mandi)
nagpur_mandi = df_mandi_all[df_mandi_all['district_name'].str.upper() == 'NAGPUR'].sort_values(['APMC', 'date'])
cols_mandi = ['APMC', 'Commodity', 'date', 'arrivals_in_qtl', 'min_price', 'max_price', 'modal_price']
print('\n=== 3. MANDI 20 ROWS ===')
print(nagpur_mandi[cols_mandi].head(20).to_markdown(index=False))

# 4. Open-Meteo forecast (first 14 rows: 14 tehsils forecast)
print('\n=== 4. OPEN-METEO FORECAST ROWS ===')
tehsils = [
    ('Ramtek', 21.51508, 79.34985),
    ('Umred', 20.85107, 79.19023),
    ('Nagpur (rural)', 21.02600, 78.99752),
    ('Hingna', 21.00230, 78.86729),
    ('Katol', 21.23028, 78.63156),
    ('Bhiwapur', 20.72717, 79.37088),
    ('Kalameshwar', 21.27613, 78.85215),
    ('Kuhi', 20.98193, 79.44755),
    ('Savner', 21.41714, 78.94767),
    ('Kamptee', 21.14488, 79.24463),
    ('Parseoni', 21.43279, 79.14782),
    ('Nagpur (urban)', 21.14466, 79.07992),
    ('Narkhed', 21.38584, 78.48836),
    ('Mauda', 21.22788, 79.43532)
]
forecast_rows = []
for name, lat, lon in tehsils:
    r_fc = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Asia%2FKolkata", timeout=10)
    data = r_fc.json()
    daily = data.get('daily', {})
    if daily and 'time' in daily:
        t0 = daily['time'][0]
        p0 = daily['precipitation_sum'][0]
        tmax0 = daily['temperature_2m_max'][0]
        tmin0 = daily['temperature_2m_min'][0]
        forecast_rows.append({'Tehsil': name, 'Date': t0, 'Lat': lat, 'Lon': lon, 'T_Max (C)': tmax0, 'T_Min (C)': tmin0, 'Rain (mm)': p0})
print(pd.DataFrame(forecast_rows).to_markdown(index=False))

