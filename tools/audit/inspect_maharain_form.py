import requests, urllib3, re
urllib3.disable_warnings()

url = 'https://maharain.maharashtra.gov.in/test/maharain/report_tehsil_wise_report_june_september.php'
r = requests.get(url, verify=False, timeout=10)
print(re.findall(r'<script\b[^>]*src="([^"]+)"', r.text))
# Print the body container
body_match = re.search(r'<body\b[^>]*>(.*?)</body>', r.text, re.DOTALL)
if body_match:
    print('Body excerpt:')
    print(re.sub(r'\s+', ' ', body_match.group(1))[:1000])
