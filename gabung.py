import requests

URL1 = "https://raw.githubusercontent.com/rohmanabdu/deqiaa/refs/heads/main/hasill"
URL2 = "https://raw.githubusercontent.com/rohmanabdu/deqiaa/refs/heads/main/pll/ramaa2"
OUTPUT = "desafirax"  # hasil gabungan akan timpa file ini

def fetch(url):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"Gagal ambil {url}: {e}")
        return ""

def parse_m3u(content):
    lines = content.splitlines()
    channels = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            info = line
            url = lines[i+1].strip() if i+1 < len(lines) else ""
            channels.append((info, url))
            i += 2
        else:
            i += 1
    return channels

def gabung():
    print("Ambil playlist 1...")
    c1 = fetch(URL1)
    print("Ambil playlist 2...")
    c2 = fetch(URL2)

    ch1 = parse_m3u(c1)
    ch2 = parse_m3u(c2)

    print(f"Playlist 1: {len(ch1)} channel")
    print(f"Playlist 2: {len(ch2)} channel")

    # Gabung + anti duplikat berdasarkan URL stream
    seen_url = set()
    all_channels = []
    for info, url in ch1 + ch2:
        if url and url not in seen_url and url.startswith("http"):
            seen_url.add(url)
            all_channels.append((info, url))

    print(f"Hasil gabungan: {len(all_channels)} channel unik")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for info, url in all_channels:
            f.write(f"{info}\n{url}\n")

    print(f"Sukses! Disimpan ke {OUTPUT}")

if __name__ == "__main__":
    gabung()
