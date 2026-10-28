import requests

url = 'https://www.msamb.com/ApmcDirectory/APMCList'
r = requests.get(url, timeout=10)
print(r.text.encode('ascii', 'ignore').decode('ascii'))
