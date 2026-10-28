import requests, re

r = requests.get('https://agmarknet.gov.in/static/js/main.c1f86740.js', timeout=10)
# Look for any URL with http or fetch/axios
urls = re.findall(r'https?://[a-zA-Z0-9_\-\./:]+', r.text)
for u in set(urls):
    print(u)
