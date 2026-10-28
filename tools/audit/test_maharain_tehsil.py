import requests, urllib3
urllib3.disable_warnings()

url = 'https://maharain.maharashtra.gov.in/test/maharain/report_tehsil_wise_report_june_september.php'
r = requests.get(url, verify=False, timeout=10)
print('Status:', r.status_code, len(r.text))
if 'Nagpur' in r.text or 'नागपूर' in r.text:
    print('Found Nagpur in tehsil report!')
    pos = r.text.find('Nagpur') if 'Nagpur' in r.text else r.text.find('नागपूर')
    print(r.text[pos-100:pos+300])
else:
    print('First 300 chars:')
    print(r.text[:300])
