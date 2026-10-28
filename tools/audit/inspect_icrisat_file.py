import requests

url_info = 'https://api.github.com/repos/Praneet2003/Agriculture-Data-Analysis-with-Python/contents/ICRISAT-District Level Data (Python).csv'
r = requests.get(url_info, headers={'User-Agent': 'Antigravity'})
print('ICRISAT CSV file size:', r.json().get('size'))
print('Download URL:', r.json().get('download_url'))

r_amar = requests.get('https://api.github.com/repos/amar-at-iitm/ma5755-capstone-project/contents/data', headers={'User-Agent': 'Antigravity'})
print('Amar data contents:', [x['name'] for x in r_amar.json()])
