import pandas as pd

url = 'https://raw.githubusercontent.com/Praneet2003/Agriculture-Data-Analysis-with-Python/main/ICRISAT-District%20Level%20Data%20(Python).csv'
# Read header only first
df_head = pd.read_csv(url, nrows=10)
print('Columns:', df_head.columns.tolist()[:30])
print('Shape preview:')
print(df_head.head(2))

# Now let's filter for Nagpur
df = pd.read_csv(url)
nagpur_rows = df[df['Dist Name'].str.upper() == 'NAGPUR'] if 'Dist Name' in df.columns else df[df['District'].str.upper() == 'NAGPUR']
print('Total Nagpur rows in ICRISAT:', len(nagpur_rows))
print('Years covered in ICRISAT for Nagpur:', nagpur_rows['Year'].min(), 'to', nagpur_rows['Year'].max())
print('Nagpur columns sample:')
print(nagpur_rows[['Year', 'SOYABEAN AREA (1000 ha)', 'SOYABEAN PRODUCTION (1000 tons)', 'SOYABEAN YIELD (Kg per ha)', 'COTTON AREA (1000 ha)', 'COTTON PRODUCTION (1000 tons)', 'COTTON YIELD (Kg per ha)', 'RICE AREA (1000 ha)', 'RICE PRODUCTION (1000 tons)', 'RICE YIELD (Kg per ha)']].head(15))
