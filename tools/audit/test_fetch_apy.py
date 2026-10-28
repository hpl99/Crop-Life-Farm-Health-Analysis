import requests, urllib3, re
urllib3.disable_warnings()

s = requests.Session()
s.verify = False

r1 = s.get('https://data.desagri.gov.in/website/crops-report-district-level-web', timeout=10)
token_match = re.search(r'id="hdnrltoken"[^>]+value="([^"]+)"', r1.text)
token = token_match.group(1) if token_match else ''

payload = {
    'fltrstates': '27', # Maharashtra
    'fltrcrops': '4',    # Oilseeds
    'fltrstartyear': '2015',
    'fltrendyear': '2022',
    'fltrrptformat': 'scrview',
    '_token': token
}

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://data.desagri.gov.in/website/crops-report-district-level-web'
}

r2 = s.post('https://data.desagri.gov.in/report/crop/report-district-level', data=payload, headers=headers, timeout=20)
print('POST status:', r2.status_code, len(r2.text))
if 'Nagpur' in r2.text:
    print('Found Nagpur in table!')
    # Print a snippet of Nagpur row
    pos = r2.text.find('Nagpur')
    print(r2.text[pos-100:pos+400])
else:
    print('First 500 chars of response:')
    print(r2.text[:500])
