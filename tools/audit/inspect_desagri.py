import requests, urllib3, re
urllib3.disable_warnings()

r = requests.get('https://data.desagri.gov.in/website/crops-apy-report-web', verify=False, timeout=10)
print('Status:', r.status_code)
# Search for API URLs or form endpoints
matches = re.findall(r'(\/[a-zA-Z0-9_\-\/]+(?:api|report|get|data|crop)[a-zA-Z0-9_\-\/]*)', r.text)
print('Matched endpoints in JS/HTML:', set(matches))
