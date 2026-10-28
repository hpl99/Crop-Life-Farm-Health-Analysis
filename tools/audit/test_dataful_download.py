import requests, re

r = requests.get('https://dataful.in/datasets/5632/', timeout=10)
# Find mentions of download, or auth, or login, or cart, or price
matches = re.findall(r'([^.]{0,100}download[^.]{0,100})', r.text, re.IGNORECASE)
for m in matches[:10]:
    print('-', m.strip())
