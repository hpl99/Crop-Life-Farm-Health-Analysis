import requests, io
import pandas as pd

url = 'https://raw.githubusercontent.com/joshi-vipul/maharashtra_mandi/master/CMO_MSP_Mandi.csv'
r = requests.get(url, timeout=10)
print('CMO_MSP_Mandi.csv status:', r.status_code, len(r.content))
df = pd.read_csv(io.StringIO(r.text))
print('Columns:', df.columns.tolist())
print(df.head(5))

url2 = 'https://raw.githubusercontent.com/joshi-vipul/maharashtra_mandi/master/Monthly_data_cmo.csv'
# Inspect header first
r2 = requests.get(url2, headers={'Range': 'bytes=0-10000'})
print('Monthly_data_cmo.csv range status:', r2.status_code)
df2 = pd.read_csv(io.StringIO(r2.text), nrows=10)
print('Monthly_data_cmo columns:', df2.columns.tolist())
print(df2.head(2))
