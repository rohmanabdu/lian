import requests
import re

URL1 = "https://raw.githubusercontent.com/rohmanabdu/deqiaa/refs/heads/main/hasill"
URL2 = "https://raw.githubusercontent.com/rohmanabdu/deqiaa/refs/heads/main/pll/ramaa2"
OUTPUT = "hasill"

# === GANTI NAMA FOLDER DISINI ===
# Ini nama baru buat kategori "upcoming" dari url 2
NAMA_BARU_URL2 = "Live Event 2"  # <-- GANTI SESUKA LU

def fetch(url):
    try:
        print(f"Fetching {url}...")
        r = requests.get(url, timeout=30)
        print(f"Status {url}: {r.status_code}, size: {len(r.text)}")
        if r.status_code == 200:
            return r.text
        return ""
    except Exception as e:
        print(f"Error {url}: {e}")
        return ""

def clean(content):
    lines = []
    for line in content.splitlines():
        if line.strip().upper() == "#EXTM3U":
            continue
        if line.strip() == "":
            continue
        lines.append(line)
    return "\n".join(lines)

def rename_upcoming(content, new_name):
    # ganti semua group-title yang mengandung kata upcoming / UPCOMING / Upcoming
    # jadi nama baru
    def replacer(match):
        return f'group-title="{new_name}"'
    
    # ini akan ganti group-title="Upcoming" atau group-title="UPCOMING EVENT" dll
    content = re.sub(
        r'group-title="[^"]*upcoming[^"]*"', 
        replacer, 
        content, 
        flags=re.IGNORECASE
    )
    # kalau ada yang pakai group-title='Upcoming' pakai kutip 1
    content = re.sub(
        r"group-title='[^']*upcoming[^']*'", 
        f"group-title=\"{new_name}\"", 
        content, 
        flags=re.IGNORECASE
    )
    return content

def gabung():
    c1 = fetch(URL1)
    c2 = fetch(URL2)

    if not c1 and not c2:
        print("KEDUA FILE KOSONG! Cek link raw nya!")
        return

    # URL1 biarin apa adanya
    cleaned1 = clean(c1)
    
    # URL2 kita ganti nama folder upcoming nya dulu baru dibersihin
    print(f"Mengganti folder 'Upcoming' di URL2 menjadi '{NAMA_BARU_URL2}'...")
    c2_renamed = rename_upcoming(c2, NAMA_BARU_URL2)
    cleaned2 = clean(c2_renamed)

    final = "#EXTM3U\n" + cleaned1 + "\n" + cleaned2 + "\n"

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(final)

    print(f"SUKSES! {OUTPUT} size: {len(final)} char")

if __name__ == "__main__":
    gabung()
