import requests

base = 'https://raw.githubusercontent.com/arulalant/India-BlockLevel-SubDistricts-Shape-File/master/'
# Check file sizes
r = requests.get('https://api.github.com/repos/arulalant/India-BlockLevel-SubDistricts-Shape-File/contents', headers={'User-Agent': 'Antigravity'})
for f in r.json():
    print(f['name'], f['size'])
