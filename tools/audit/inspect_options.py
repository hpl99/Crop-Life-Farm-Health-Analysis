import requests, urllib3, re
urllib3.disable_warnings()

r = requests.get('https://data.desagri.gov.in/website/crops-report-district-level-web', verify=False, timeout=10)
# Find options in select id="fltrstates"
states = re.findall(r'<select[^>]+id="fltrstates"[^>]*>(.*?)</select>', r.text, re.DOTALL)
if states:
    print('States options:')
    for val, name in re.findall(r'<option[^>]+value="([^"]*)"[^>]*>(.*?)</option>', states[0]):
        if 'Maharashtra' in name:
            print(f"State: {name} -> {val}")

crops = re.findall(r'<select[^>]+id="fltrcrops"[^>]*>(.*?)</select>', r.text, re.DOTALL)
if crops:
    print('Crops options:')
    for val, name in re.findall(r'<option[^>]+value="([^"]*)"[^>]*>(.*?)</option>', crops[0]):
        if any(c in name.lower() for c in ['soy', 'cott', 'rice', 'oil']):
            print(f"Crop: {name} -> {val}")

years = re.findall(r'<select[^>]+id="fltrstartyear"[^>]*>(.*?)</select>', r.text, re.DOTALL)
if years:
    print('Years options (sample):')
    for val, name in re.findall(r'<option[^>]+value="([^"]*)"[^>]*>(.*?)</option>', years[0])[:5]:
        print(f"Year: {name} -> {val}")

token = re.findall(r'id="hdnrltoken"[^>]+value="([^"]+)"', r.text)
print('Token:', token)
