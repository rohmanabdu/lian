import re
from urllib.request import Request, urlopen

URL = "https://rebrand.ly/UPPL2026"

req = Request(URL, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
})
with urlopen(req, timeout=60) as resp:
    text = resp.read().decode("utf-8", errors="ignore").lstrip("\ufeff")

lines = text.splitlines()

from collections import Counter
groups = Counter()
kept = 0
skipped = 0

i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("#EXTINF"):
        block = [line]
        j = i + 1
        url_found = False
        while j < len(lines):
            nxt = lines[j].strip()
            if nxt.startswith("#EXTINF"):
                break
            block.append(nxt)
            if nxt.startswith("http://") or nxt.startswith("https://"):
                url_found = True
                j += 1
                break
            j += 1

        group = ""
        m = re.search(r'group-title="([^"]+)"', line)
        if m:
            group = m.group(1)
        name = line.split(",", 1)[1].strip() if "," in line else ""
        groups[group] += 1

        if ("EVENT" in group.upper()
            and "CADANGAN" not in group.upper()
            and "001 TRAKTIR KOPI" not in name.upper()
            and url_found):
            kept += 1
        else:
            if kept < 5 or skipped < 5:
                print(f"SKIPPED -> group='{group}' | name='{name}' | url_found={url_found} | block_len={len(block)}")
            skipped += 1
        i = j
    else:
        i += 1

print(f"Diambil: {kept}, Dibuang: {skipped}")
print("\n=== SEMUA GROUP-TITLE YANG ADA ===")
for g, c in groups.most_common(50):
    print(f"{c} x '{g}'")
