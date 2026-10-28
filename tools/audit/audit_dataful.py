import requests
import re

datasets = ['19215', '19226', '3780', '3784', '3902', '4163', '4885', '5185', '5405', '5606', '5632', '606']
for d in datasets:
    try:
        r = requests.get(f'https://dataful.in/datasets/{d}/', timeout=10)
        title = re.search(r'<h1[^>]*>(.*?)</h1>', r.text, re.DOTALL)
        t_text = title.group(1).strip() if title else 'No title'
        t_text = re.sub(r'<[^>]+>', '', t_text)
        print(f"Dataset {d}: {t_text}")
    except Exception as e:
        print(f"Dataset {d} err: {e}")
