import requests
import re
import json

url = 'https://dataful.in/datasets/5632/'
r = requests.get(url, timeout=10)
print('Status:', r.status_code)
# Search for download links or API endpoints
links = re.findall(r'href="([^"]+)"', r.text)
for l in links:
    if 'download' in l or 'csv' in l or 'api' in l or 'resources' in l or 'file' in l:
        print('Resource link:', l)

# Also check page text for source, license, frequency, coverage
lines = [line.strip() for line in r.text.split('\n') if any(k in line.lower() for k in ['source', 'license', 'frequency', 'published', 'department', 'coverage', 'year'])]
print('\nRelevant metadata snippets:')
for line in lines[:25]:
    cleaned = re.sub(r'<[^>]+>', ' ', line).strip()
    if cleaned and len(cleaned) > 5:
        print('-', cleaned)
