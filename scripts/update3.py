import os
import requests
import re

URL = "https://rebrand.ly/UPPL2026"
OUT_DIR = "playlist"
OUT_FILE = os.path.join(OUT_DIR, "rama2.m3u")
os.makedirs(OUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
resp = requests.get(URL, headers=headers, timeout=30, allow_redirects=True)
resp.raise_for_status()
text = resp.text.lstrip("\ufeff")

lines = [l.strip() for l in text.splitlines() if l.strip()]
result = ["#EXTM3U"]

total = 0
kept = 0
deleted_traktir = 0
deleted_cadangan = 0

i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("#EXTINF:"):
        extinf = line
        url = lines[i+1] if i+1 < len(lines) else ""

        # Jika baris berikutnya bukan URL (misal #EXTINF lagi), skip
        if url.startswith("#"):
            i += 1
            continue

        total += 1

        # Ambil group-title
        group_match = re.search(r'group-title="([^"]*)"', extinf, re.IGNORECASE)
        group = group_match.group(1).upper() if group_match else ""

        # Ambil nama channel (setelah koma terakhir)
        channel_name = extinf.rsplit(",", 1)[-1].strip().upper() if "," in extinf else ""

        # 1. HAPUS CADANGAN EVENT
        is_cadangan = "CADANGAN" in group or "CADANGAN" in channel_name

        # 2. HAPUS TRAKTIR KOPI (traktir / traktik)
        is_traktir = "TRAKTIR" in channel_name or "TRAKTIK" in channel_name or "TRAKTIR KOPI" in channel_name

        # 3. HANYA EVENT ASLI
        is_event = "EVENT" in group

        if is_event and not is_cadangan and not is_traktir:
            result.append(extinf)
            result.append(url)
            kept += 1
        else:
            if is_traktir:
                deleted_traktir += 1
            if is_cadangan:
                deleted_cadangan += 1

        i += 2
    else:
        i += 1

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print(f"Total channel dari link: {total}")
print(f"Disimpan ke rama2.m3u: {kept}")
print(f"Dibuang (001 TRAKTIR KOPI): {deleted_traktir}")
print(f"Dibuang (CADANGAN EVENT): {deleted_cadangan}")
