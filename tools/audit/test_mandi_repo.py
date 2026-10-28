import requests, io
import pandas as pd

url = 'https://raw.githubusercontent.com/Sheetalkandhare/Agmarknet/master/Agmarket_assg.csv'
r = requests.get(url)
print('status:', r.status_code, len(r.content))
if r.status_code == 200:
    df = pd.read_csv(io.StringIO(r.text))
    print('Columns:', df.columns.tolist())
    print('Districts:', df['District Name'].unique()[:10] if 'District Name' in df.columns else 'no col')
    nagpur = df[df['District Name'].str.upper() == 'NAGPUR'] if 'District Name' in df.columns else pd.DataFrame()
    print('Nagpur count:', len(nagpur))
    if len(nagpur) > 0:
        print(nagpur.head(5))
