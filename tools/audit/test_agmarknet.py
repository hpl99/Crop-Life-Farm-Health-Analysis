import requests

# Test Agmarknet direct or open datasets
urls = [
    'https://agmarknet.gov.in',
    'http://agmarknet.gov.in',
    'https://raw.githubusercontent.com/datasets/agmarknet/master/data.csv'
]
for u in urls:
    try:
        r = requests.get(u, timeout=5)
        print(u, r.status_code)
    except Exception as e:
        print(u, e)
