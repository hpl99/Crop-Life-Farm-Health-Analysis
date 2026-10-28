import requests, urllib3, re
urllib3.disable_warnings()

r = requests.get('https://maharain.maharashtra.gov.in', verify=False, timeout=10)
# Look at the actual <a href="..."> tags with their relative paths
for m in re.finditer(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r.text, re.DOTALL):
    href, text = m.group(1), m.group(2).strip()
    if 'tehsil' in href.lower() or 'district' in href.lower():
        print(href, '-->', re.sub(r'\s+', ' ', text))
