import requests

r = requests.get('https://dataful.in/datasets/5632/', timeout=10)
pos = r.text.find(r'\"dataset\":')
raw = r.text[pos:pos+20000]

# Let's find any keys or file paths
import re
print("Keys/fields:")
print(re.findall(r'\\\"([a-zA-Z0-9_\-]+)\\\":', raw)[:40])
print("\nFiles/URLs:")
for m in re.finditer(r'(https?://[^\s\\"]+|/[^\s\\"]+\.(?:csv|xlsx|parquet|json))', raw):
    print(m.group(1))
