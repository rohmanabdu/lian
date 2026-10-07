import requests

# Ambil playlist pakai curl, bukan requests (biar tidak 403)
URL = "https://rebrand.ly/UPPL2026"
TMP_FILE = "/tmp/source.m3u"
OUT_DIR = "playlist"
OUT_FILE = os.path.join(OUT_DIR, "rama3.m3u")
os.makedirs(OUT_DIR, exist_ok=True)

# Coba curl dengan header Chrome asli
cmd = [
    "curl", "-sL", "--compressed",
    "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "-H", "Accept-Language: en-US,en;q=0.9,id;q=0.8",
    "-H", "Referer: https://www.google.com/",
    "--max-time", "30",
    URL, "-o", TMP_FILE
]
subprocess.run(cmd, check=True)

with open(TMP_FILE, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read().lstrip("\ufeff")

lines = [l.rstrip() for l in text.splitlines() if l.strip()]
print(f"Total baris terdownload: {len(lines)}")

result = ["#EXTM3U"]
total = 0
kept = 0

i = 0
while i < len(lines):
    if lines[i].startswith("#EXTINF:"):
        block = [lines[i]]
        i += 1
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

        if not is_traktir and not is_cadangan:
            result.extend(block)
            kept += 1
    else:
        i += 1

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result) + "\n")

print(f"=== total={total} disimpan={kept} -> {OUT_FILE} ===")
