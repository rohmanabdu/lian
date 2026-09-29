import requests
import os

# ================== CONFIG ==================
SOURCE_URL = "https://liveloveyou.my.id/137286ec/lv.txt"
OUTPUT_FILE = "playlist/rama2.m3u"  # <-- NAMA BARU SESUAI REQUEST

# Tulisan yang ingin dihapus
REMOVE_TEXT = "Gvision TV"

# DAFTAR LOGO YANG DIGANTI
LOGO_REPLACEMENTS = [
    {
        "old": "https://wsrv.nl/?url=https%3A%2F%2Fi.ibb.co.com%2FrGySkbHm%2F20260806-155101.png&bg=FFFFFF",
        "new": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT26xVe6CPgwgTjD5OmiZeVDi7QQbZduKWYb7OZmYm9jEL_xlQxK7p6G5rl&s=10"
    },
    {
        "old": "https://i.ibb.co.com/d15rKps/20260701-044822.jpg",
        "new": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT26xVe6CPgwgTjD5OmiZeVDi7QQbZduKWYb7OZmYm9jEL_xlQxK7p6G5rl&s=10"
    },
    {
        "old": "https://wsrv.nl/?url=https%3A%2F%2Fi.ibb.co.com%2FrGySkbHm%2F20260806-155101.png&bg=00FA9A",
        "new": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT26xVe6CPgwgTjD5OmiZeVDi7QQbZduKWYb7OZmYm9jEL_xlQxK7p6G5rl&s=10"
    },
    {
        "old": "https://i.ibb.co.com/LXD7m275/20260730-120141.jpg",
        "new": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT26xVe6CPgwgTjD5OmiZeVDi7QQbZduKWYb7OZmYm9jEL_xlQxK7p6G5rl&s=10"
    },
    {
        "old": "https://wsrv.nl/?url=https%3A%2F%2Fi.ibb.co.com%2FrGySkbHm%2F20260806-155101.png&bg=FF1493",
        "new": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT26xVe6CPgwgTjD5OmiZeVDi7QQbZduKWYb7OZmYm9jEL_xlQxK7p6G5rl&s=10"
    },
]
# ============================================

def main():
    os.makedirs("playlist", exist_ok=True)
    
    print(f"Ambil: {SOURCE_URL}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/plain,*/*"
    }
    r = requests.get(SOURCE_URL, headers=headers, timeout=30)
    r.raise_for_status()
    playlist = r.text
    print(f"Awal: {len(playlist)} char")

    # 1. HAPUS TULISAN Gvision TV
    playlist = playlist.replace(REMOVE_TEXT, "")

    # 2. BERSIHKAN TANDA |
    playlist = playlist.replace("| ", "").replace(" |", "")

    # 3. GANTI SEMUA LOGO
    for logo in LOGO_REPLACEMENTS:
        if logo.get("old") and logo.get("new"):
            playlist = playlist.replace(logo["old"], logo["new"])

    # 4. BERSIHKAN SPASI BERLEBIH
    playlist = "\n".join([line.rstrip() for line in playlist.split("\n")])

    # 5. PASTIKAN NEWLINE DI AKHIR
    if not playlist.endswith("\n"):
        playlist += "\n"

    # 6. PASTIKAN ADA #EXTM3U
    if not playlist.strip().startswith("#EXTM3U"):
        playlist = "#EXTM3U\n" + playlist

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"SELESAI -> {OUTPUT_FILE} siap, {len(playlist.splitlines())} baris")

if __name__ == "__main__":
    main()
