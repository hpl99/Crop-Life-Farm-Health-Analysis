import requests, json

url = 'https://ckandev.indiadataportal.com/api/3/action/datastore_search'
params = {
    'resource_id': '6f70d961-3a4f-4caa-b08f-f72f708791e1',
    'filters': json.dumps({'district_name': 'Nagpur'}),
    'limit': 500
}
r = requests.get(url, params=params, timeout=15)
records = r.json()['result']['records']
print('Total fetched:', len(records))

years = set(r['year'] for r in records)
print('Years:', sorted(years))

crops = set(r['crop_name'] for r in records)
print('Crops:', sorted(crops))

# Check Soybean, Cotton, Rice
for crop in ['Soyabean', 'Soybean', 'Cotton', 'Cotton(lint)', 'Rice']:
    crop_recs = [r for r in records if crop.lower() in r['crop_name'].lower()]
    print(f"\nCrop: {crop} ({len(crop_recs)} records)")
    for cr in crop_recs[:5]:
        print(f"  {cr['year']} | {cr['season']} | Area: {cr['area']} ha | Prod: {cr['production']} t | Yield: {cr['yield']} kg/ha")
