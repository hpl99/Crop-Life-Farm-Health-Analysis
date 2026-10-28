import requests, urllib3, re
urllib3.disable_warnings()

r = requests.get('https://data.desagri.gov.in/website/crops-report-district-level-web', verify=False, timeout=10)
crops = re.findall(r'<select[^>]+id="fltrcrops"[^>]*>(.*?)</select>', r.text, re.DOTALL)
if crops:
    for val, name in re.findall(r'<option[^>]+value="([^"]*)"[^>]*>(.*?)</option>', crops[0]):
        print(f"Crop group: {name} -> {val}")
