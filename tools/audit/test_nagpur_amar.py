import requests, io
import pandas as pd

base = 'https://raw.githubusercontent.com/amar-at-iitm/ma5755-capstone-project/main/data/raw/'

r_norm = requests.get(base + 'normal_rainfall_data.csv')
df_norm = pd.read_csv(io.StringIO(r_norm.text))
nagpur_norm = df_norm[df_norm['Dist Name'].str.upper() == 'NAGPUR']
print('=== NORMAL RAINFALL FOR NAGPUR ===')
print(nagpur_norm.head(2))

r_rain = requests.get(base + 'monthly_rainfall_data.csv')
df_rain = pd.read_csv(io.StringIO(r_rain.text))
nagpur_rain = df_rain[df_rain['Dist Name'].str.upper() == 'NAGPUR']
print('=== MONTHLY RAINFALL FOR NAGPUR ===')
print('Years:', nagpur_rain['Year'].min(), 'to', nagpur_rain['Year'].max(), 'Count:', len(nagpur_rain))
print(nagpur_rain[['Year', 'JUNE RAINFALL (Millimeters)', 'JULY RAINFALL (Millimeters)', 'AUGUST RAINFALL (Millimeters)', 'SEPTEMBER RAINFALL (Millimeters)']].tail(10))

r_apy = requests.get(base + 'area_production_yield_data.csv')
df_apy = pd.read_csv(io.StringIO(r_apy.text))
nagpur_apy = df_apy[df_apy['Dist Name'].str.upper() == 'NAGPUR']
print('=== APY FOR NAGPUR ===')
print('Years:', nagpur_apy['Year'].min(), 'to', nagpur_apy['Year'].max(), 'Count:', len(nagpur_apy))
print(nagpur_apy[['Year', 'SOYABEAN AREA (1000 ha)', 'SOYABEAN YIELD (Kg per ha)', 'COTTON AREA (1000 ha)', 'COTTON YIELD (Kg per ha)', 'RICE AREA (1000 ha)', 'RICE YIELD (Kg per ha)']].tail(10))
