import requests, io
import pandas as pd

url = 'https://raw.githubusercontent.com/joshi-vipul/maharashtra_mandi/master/Monthly_data_cmo.csv'
r = requests.get(url)
df = pd.read_csv(io.StringIO(r.text))
print('Total rows:', len(df))
nagpur = df[df['district_name'].str.upper() == 'NAGPUR']
print('Nagpur rows:', len(nagpur))
print('Nagpur APMCs:', nagpur['APMC'].unique().tolist())
print('Nagpur Commodities:', nagpur['Commodity'].unique().tolist())
print('Nagpur date range:', nagpur['date'].min(), 'to', nagpur['date'].max())
print('Nagpur Soybean sample:')
print(nagpur[nagpur['Commodity'].str.contains('Soy', case=False)].head(10))
