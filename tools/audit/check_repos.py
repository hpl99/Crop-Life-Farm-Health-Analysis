import requests

repos = [
    'Sakthivel-67/i-have-the-icrisat-district-level-agricultural',
    'Praneet2003/Agriculture-Data-Analysis-with-Python',
    'ekankshyellala/icrisat-crop-analysis',
    'amar-at-iitm/ma5755-capstone-project'
]
for repo in repos:
    r = requests.get(f'https://api.github.com/repos/{repo}/contents', headers={'User-Agent': 'Antigravity'}, timeout=10)
    print(repo, [x['name'] for x in r.json() if isinstance(r.json(), list)])
