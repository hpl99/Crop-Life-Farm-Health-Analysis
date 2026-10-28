import requests, io
import pandas as pd

base = 'https://raw.githubusercontent.com/amar-at-iitm/ma5755-capstone-project/main/data/raw/'
for f in ['normal_rainfall_data.csv', 'monthly_rainfall_data.csv', 'area_production_yield_data.csv']:
    r = requests.get(base + f)
    print(f, 'size:', len(r.content))
    df = pd.read_csv(io.StringIO(r.text), nrows=5)
    print(f, 'columns:', df.columns.tolist()[:10])
