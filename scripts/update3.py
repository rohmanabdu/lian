import os
import requests
import re

URL = "https://rebrand.ly/UPPL2026"
OUT_DIR = "playlist"
OUT_FILE = os.path.join(OUT_DIR, "rama2.m3u")

os.makedirs(OUT_DIR, exist_ok=True)

# 1. Ambil playlist (ikut redirect rebrand.ly)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
resp = requests.get(URL, headers=headers, timeout=30, allow_redirects=True)
resp.raise_for_status()
text = resp.text

# Hapus BOM jika ada
if text.startswith("\ufeff"):
    text = text.lstrip("\ufeff")

lines = text.splitlines()

result = ["#EXTM3U"]

# Regex ambil nama channel & group
# Contoh: #EXTINF:-1 tvg-name="..." group-title="EVENT..." ,001 TRAKTIR KOPI
current_extinf = None

for line in lines:
    line = line.strip()
    if not line:
        continue

    if line.startswith("#EXTINF:"):
        current_extinf = line
        continue

    # Jika ini URL (atau baris setelah EXTINF)
    if current_extinf is not None and not line.startswith("#"):
        # Ambil group-title
        group_match = re.search(r'group-title="([^"]*)"', current_extinf, re.IGNORECASE)
        group = group_match.group(1) if group_match else ""

        # Ambil nama channel (setelah koma terakhir)
        channel_name = ""
        if "," in current_extinf:
            channel_name = current_extinf.rsplit(",", 1)[-1].strip()

        # Cek kategori EVENT
        is_event = "EVENT" in group.upper()

        # Cek channel yang dibuang
        is_traktir = "001 TRAKTIR KOPI" in channel_name.upper()

        # Simpan hanya EVENT dan bukan TRAKTIR
        if is_event and not is_traktir:
            result.append(current_extinf)
            result.append(line)

        current_extinf = None
    else:
        current_extinf = None

# Simpan hasil
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print(f"Berhasil! Total channel EVENT (tanpa 001 TRAKTIR KOPI): {len(result)//2}")
print(f"File disimpan di: {OUT_FILE}")
