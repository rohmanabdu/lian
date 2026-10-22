import requests

URL1 = "https://raw.githubusercontent.com/rohmanabdu/deqiaa/refs/heads/main/hasill"
URL2 = "https://raw.githubusercontent.com/rohmanabdu/deqiaa/refs/heads/main/pll/ramaa2"
OUTPUT = "hasill"  # kalau mau aman, ganti jadi "hasill_gabungan.m3u"

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
    # buang header #EXTM3U biar gak dobel
    lines = []
    for line in content.splitlines():
        if line.strip().upper() == "#EXTM3U":
            continue
        if line.strip() == "":
            continue
        lines.append(line)
    return "\n".join(lines)

def gabung():
    c1 = fetch(URL1)
    c2 = fetch(URL2)

    if not c1 and not c2:
        print("KEDUA FILE KOSONG! Cek link raw nya!")
        return

    cleaned1 = clean(c1)
    cleaned2 = clean(c2)

    # gabung tanpa hapus duplikat dulu, biar gak kosong
    final = "#EXTM3U\n" + cleaned1 + "\n" + cleaned2 + "\n"

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(final)

    print(f"SUKSES! {OUTPUT} size: {len(final)} char")
    print(f"Preview 5 baris pertama:\n{final[:500]}")

if __name__ == "__main__":
    gabung()
