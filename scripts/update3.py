import os, requests, re

URL = "https://rebrand.ly/UPPL2026"
OUT_DIR = "playlist"
OUT_FILE = os.path.join(OUT_DIR, "rama3.m3u")
os.makedirs(OUT_DIR, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(URL, headers=headers, timeout=30, allow_redirects=True)
resp.raise_for_status()
text = resp.text.lstrip("\ufeff")
lines = [l.rstrip() for l in text.splitlines() if l.strip()]

result = ["#EXTM3U"]
total = 0
kept = 0

i = 0
while i < len(lines):
    if lines[i].startswith("#EXTINF:"):
        block = [lines[i]]
        i += 1
        # Ambil semua baris sampai EXTINF berikutnya (termasuk #EXTVLCOPT, dll dan URL)
        while i < len(lines) and not lines[i].startswith("#EXTINF:"):
            block.append(lines[i])
            i += 1

        extinf = block[0]
        total += 1

        group_match = re.search(r'group-title="([^"]*)"', extinf, re.IGNORECASE)
        group = (group_match.group(1) if group_match else "").upper()
        name = (extinf.rsplit(",",1)[-1].strip() if "," in extinf else "").upper()

        is_traktir = "TRAKTIR" in name or "TRAKTIK" in name
        is_cadangan = "CADANGAN" in group or "CADANGAN" in name

        print(f"[{total}] GROUP='{group}' | NAME='{name}' -> {'DIBUANG' if (is_traktir or is_cadangan) else 'DISIMPAN'}")

        # HANYA 2 yang dibuang, sisanya semua disimpan
        if not is_traktir and not is_cadangan:
            result.extend(block)
            kept += 1
    else:
        i += 1

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print(f"=== total={total} disimpan={kept} ===")
