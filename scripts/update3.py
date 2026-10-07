import os
import re
from urllib.request import Request, urlopen

URL = "https://rebrand.ly/UPPL2026"
OUT_DIR = "playlist"
OUT_FILE = os.path.join(OUT_DIR, "rama3.m3u")

os.makedirs(OUT_DIR, exist_ok=True)

req = Request(URL, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
})
with urlopen(req, timeout=60) as resp:
    text = resp.read().decode("utf-8", errors="ignore").lstrip("\ufeff")

lines = text.splitlines()
result = ["#EXTM3U"]
kept = 0
skipped = 0

i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("#EXTINF"):
        # Kumpulkan 1 blok: EXTINF + semua baris tambahan sampai ketemu URL
        block = [line]
        j = i + 1
        url_found = False
        while j < len(lines):
            nxt = lines[j].strip()
            # Kalau ketemu EXTINF baru, blok selesai
            if nxt.startswith("#EXTINF"):
                break
            block.append(nxt)
            # URL adalah baris yang diawali http/https
            if nxt.startswith("http://") or nxt.startswith("https://"):
                url_found = True
                j += 1
                break
            j += 1

        # === FILTER ===
        group = ""
        m = re.search(r'group-title="([^"]+)"', line)
        if m:
            group = m.group(1)
        name = line.split(",", 1)[1].strip() if "," in line else ""

        if ("EVENT" in group.upper()
            and "CADANGAN" not in group.upper()
            and "001 TRAKTIR KOPI" not in name.upper()
            and url_found):
            result.extend(block)
            kept += 1
        else:
            skipped += 1

        i = j
    else:
        i += 1

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print(f"Diambil: {kept}, Dibuang: {skipped}, Saved -> {OUT_FILE}")
