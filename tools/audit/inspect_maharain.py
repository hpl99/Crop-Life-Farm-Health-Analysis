import requests, urllib3, re
urllib3.disable_warnings()

r = requests.get('https://maharain.maharashtra.gov.in', verify=False, timeout=10)
print('Title:', re.findall(r'<title>(.*?)</title>', r.text, re.IGNORECASE))
links = re.findall(r'href="([^"]+)"', r.text)
for l in set(links):
    if any(k in l.lower() for k in ['rain', 'report', 'circle', 'taluka', 'district', 'data']):
        print('Link:', l)
