import requests

base = 'https://api.agmarknet.gov.in/v1/'
urls = [
    'list-state',
    'daily-price-arrival/filters',
    'market-district-state'
]
for u in urls:
    try:
        r = requests.get(base + u, timeout=10)
        print(u, 'status:', r.status_code, len(r.text))
        if r.status_code == 200:
            print('Sample:', r.text[:300])
    except Exception as e:
        print(u, 'err:', e)
