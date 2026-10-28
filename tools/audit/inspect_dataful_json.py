import requests
import re
import json

url = 'https://dataful.in/datasets/5632/'
r = requests.get(url, timeout=10)

# Check for JSON embedded in Next.js page state
next_f = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', r.text)
print('Found next_f chunks:', len(next_f))

# Let's search inside the text for "Nagpur"
nagpur_matches = [line for line in r.text.split('\n') if 'Nagpur' in line or 'nagpur' in line]
print('Direct text mentions of Nagpur:', len(nagpur_matches))

# Let's search for download url or file url
for chunk in next_f:
    if 'download' in chunk or '.csv' in chunk or 's3' in chunk or 'storage' in chunk:
        print('Chunk with download:', chunk[:200])
