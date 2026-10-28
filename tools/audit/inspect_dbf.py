import requests, struct

url = 'https://raw.githubusercontent.com/arulalant/India-BlockLevel-SubDistricts-Shape-File/master/sub_district.dbf'
r = requests.get(url)
content = r.content

# Read DBF header
num_records, header_len, record_len = struct.unpack('<IHH', content[4:12])
print(f"Records: {num_records}, Header length: {header_len}, Record length: {record_len}")

fields = []
pos = 32
while content[pos] != 0x0D and pos < header_len:
    name = content[pos:pos+11].replace(b'\x00', b'').decode('ascii', errors='ignore')
    typ = chr(content[pos+11])
    length = content[pos+16]
    fields.append((name, typ, length))
    pos += 32

print("Fields:", fields)

# Search for Nagpur records
nagpur_records = []
pos = header_len
for i in range(num_records):
    rec = content[pos:pos+record_len]
    pos += record_len
    if b'Nagpur' in rec or b'NAGPUR' in rec:
        field_vals = {}
        offset = 1
        for fname, ftyp, flen in fields:
            val = rec[offset:offset+flen].decode('latin1', errors='ignore').strip()
            field_vals[fname] = val
            offset += flen
        nagpur_records.append((i, field_vals))

print(f"Found {len(nagpur_records)} Nagpur subdistricts:")
for idx, vals in nagpur_records:
    print(f"Index {idx}:", vals)
