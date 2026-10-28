import requests
import json

url = 'https://ckandev.indiadataportal.com/api/3/action/datastore_search'
params = {
    'resource_id': '6f70d961-3a4f-4caa-b08f-f72f708791e1',
    'filters': json.dumps({'district_name': 'Nagpur'}),
    'limit': 5
}
try:
    r = requests.get(url, params=params, timeout=10)
    print('CKAN status:', r.status_code)
    if r.status_code == 200:
        res = r.json()
        print('Total records for Nagpur:', res['result']['total'])
        for rec in res['result']['records']:
            print(rec)
except Exception as e:
    print('CKAN error:', e)
