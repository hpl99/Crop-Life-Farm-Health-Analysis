import requests, io
import pypdf

url = 'https://www.icar-crida.res.in/CP-2012/statewiseplans/Maharastra(Pdf)/PDKV,%20Akola/Nagpur.pdf'
r = requests.get(url, timeout=20)
reader = pypdf.PdfReader(io.BytesIO(r.content))

for page_num in [1, 2, 6, 9, 10, 11]:
    print(f"\n==================== FULL PAGE {page_num} ====================")
    text = reader.pages[page_num - 1].extract_text()
    print(text.encode('ascii', 'ignore').decode('ascii'))
