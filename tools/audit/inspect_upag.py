import requests

r1 = requests.get('https://raw.githubusercontent.com/piyush-bagoria018/india-crop-risk-monitor/main/data/public/ATTRIBUTION.md')
print('=== ATTRIBUTION.md ===')
print(r1.text)

r2 = requests.get('https://raw.githubusercontent.com/piyush-bagoria018/india-crop-risk-monitor/main/data/public/manifest.json')
print('=== manifest.json ===')
print(r2.text)
