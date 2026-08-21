#!/usr/bin/env python3
# Extract embedded base64 dish photos from index.html into real files.
import re, os, base64

html_path = "index.html"
out_dir = "foodimg"
os.makedirs(out_dir, exist_ok=True)

with open(html_path, encoding="utf-8") as f:
    lines = f.readlines()

b64pat = re.compile(r'data:image/(jpeg|png|webp);base64,([A-Za-z0-9+/=]+)"')
idpat = re.compile(r'\bid:\s*(\d+)')

count = 0
for i, line in enumerate(lines):
    if 'imagemUrl' not in line:
        continue
    m = b64pat.search(line)
    if not m:
        continue
    ext, b64 = m.groups()
    idm = idpat.search(line)
    name = f"dish_{idm.group(1) if idm else str(count+1)}.{ext}"
    data = base64.b64decode(b64)
    with open(os.path.join(out_dir, name), "wb") as g:
        g.write(data)
    lines[i] = line.replace(f'data:image/{ext};base64,{b64}"', f'{name}"', 1)
    count += 1

with open(html_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Extracted {count} images into {out_dir}/")
total = 0
for fn in sorted(os.listdir(out_dir)):
    sz = os.path.getsize(os.path.join(out_dir, fn))
    total += sz
    print(f"  {fn:24s} {sz:>8,} B")
print(f"Total images: {total:,} B")
print(f"New index.html size: {os.path.getsize(html_path):,} B")
