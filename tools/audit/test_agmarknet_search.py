import requests

r = requests.get('https://agmarknet.gov.in/SearchCmmMkt.aspx', timeout=10)
print('Length:', len(r.text))
print('First 500 chars:', r.text[:500])
