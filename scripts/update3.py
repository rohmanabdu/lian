import re
from urllib.request import Request, urlopen

URL = "https://rebrand.ly/UPPL2026"

req = Request(URL, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
})
with urlopen(req, timeout=60) as resp:
    text = resp.read().decode("utf-8", errors="ignore").lstrip("\ufeff")

lines = text.splitlines()

i = 0
printed = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("#EXTINF"):
        block = [line]
        j = i + 1
        while j < len(lines):
            nxt = lines[j].strip()
            if nxt.startswith("#EXTINF"):
                break
            block.append(nxt)
            if nxt.startswith("http://") or nxt.startswith("https://"):
                j += 1
                break
            j += 1

        group = ""
        m = re.search(r'group-title="([^"]+)"', line)
        if m:
            group = m.group(1)

        # Print blok EVENT / CADANGAN EVENT yang url_found-nya False
        if "EVENT" in group.upper() and printed < 5:
            has_url = any(x.startswith("http://") or x.startswith("https://") for x in block)
            if not has_url:
                printed += 1
                print("="*60)
                print(f"GROUP: {group}")
                for idx, b in enumerate(block):
                    print(f" [{idx}] {repr(b)}")
        i = j
    else:
        i += 1
