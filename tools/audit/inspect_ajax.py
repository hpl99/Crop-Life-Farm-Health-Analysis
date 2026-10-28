import requests, urllib3, re
urllib3.disable_warnings()

r = requests.get('https://data.desagri.gov.in/website/crops-report-district-level-web', verify=False, timeout=10)
for script in re.findall(r'<script\b[^>]*>(.*?)</script>', r.text, re.DOTALL):
    if 'getCropReport' in script:
        print(script)
