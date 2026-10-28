import requests, urllib3, re
urllib3.disable_warnings()

r = requests.get('https://data.desagri.gov.in/website/crops-report-district-level-web', verify=False, timeout=10)
print('Status:', r.status_code)
# Search for form fields or ajax urls
print('Form action:', re.findall(r'<form[^>]+action="([^"]+)"', r.text))
print('Ajax calls:', re.findall(r'\$\.(?:ajax|post|get)\([\'"]([^\'"]+)', r.text))
