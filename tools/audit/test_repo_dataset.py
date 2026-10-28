import requests, io
import pandas as pd

url = 'https://raw.githubusercontent.com/rohanwaghade/crop-production-in-maharashtra/master/dataset.xlsx'
r = requests.get(url, timeout=15)
df = pd.read_excel(io.BytesIO(r.content))
print('Unique districts:', df['Districts'].unique())
nagpur = df[df['Districts'].astype(str).str.contains('Nagpur', case=False)]
print('Nagpur rows:', len(nagpur))
if len(nagpur) > 0:
    print(nagpur.head(20))
