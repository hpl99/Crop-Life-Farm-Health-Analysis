import requests

r = requests.get('https://api.github.com/repos/amar-at-iitm/ma5755-capstone-project/contents/data/raw', headers={'User-Agent': 'Antigravity'})
print('Amar data/raw:', [x['name'] for x in r.json()])
r_clean = requests.get('https://api.github.com/repos/amar-at-iitm/ma5755-capstone-project/contents/data/cleaned', headers={'User-Agent': 'Antigravity'})
print('Amar data/cleaned:', [x['name'] for x in r_clean.json()])
