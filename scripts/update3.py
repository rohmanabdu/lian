import os
import re
from urllib.request import Request, urlopen

URL = "https://rebrand.ly/UPPL2026"
OUT_DIR = "playlist"
OUT_FILE = os.path.join(OUT_DIR, "rama3.m3u") # hasil di dalam folder playlist/

os.makedirs(OUT_DIR, exist_ok=True)

# Download (rebrand.ly otomatis redirect)
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
        # group-title
        group = ""
        m = re.search(r'group-title="([^"]+)"', line)
        if m:
            group = m.group(1)
        # nama channel
        name = line.split(",", 1)[1].strip() if "," in line else ""
        # url baris berikutnya
        url_line = lines[i+1].strip() if i+1 < len(lines) else ""

        # FILTER: hanya EVENT, bukan CADANGAN EVENT, bukan 001 TRAKTIR KOPI
        if ("EVENT" in group.upper()
            and "CADANGAN" not in group.upper()
            and "001 TRAKTIR KOPI" not in name.upper()
            and url_line and not url_line.startswith("#")):
            result.append(line)
            result.append(url_line)
            kept += 1
        else:
            skipped += 1
        i += 2
    else:
        i += 1

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print(f"Diambil: {kept}, Dibuang: {skipped}, Saved -> {OUT_FILE}")
