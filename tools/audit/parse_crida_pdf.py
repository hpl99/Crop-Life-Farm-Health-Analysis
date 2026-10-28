import requests, io
import pypdf

url = 'https://www.icar-crida.res.in/CP-2012/statewiseplans/Maharastra(Pdf)/PDKV,%20Akola/Nagpur.pdf'
r = requests.get(url, timeout=20)
reader = pypdf.PdfReader(io.BytesIO(r.content))
print(f"Total pages: {len(reader.pages)}")

# Print text of first 10 pages to find tables
for i in range(min(10, len(reader.pages))):
    text = reader.pages[i].extract_text()
    print(f"--- PAGE {i+1} ---")
    for line in text.split('\n'):
        if any(k in line.lower() for k in ['rainfall', 'soil', 'tehsil', 'taluk', 'soybean', 'cotton', 'rice', 'productivity', 'area']):
            print(line[:120])
