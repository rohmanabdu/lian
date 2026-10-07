import re
from urllib.request import Request, urlopen

URL = "https://rebrand.ly/UPPL2026"
req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
with urlopen(req, timeout=60) as resp:
    text = resp.read().decode("utf-8", errors="ignore").lstrip("\ufeff")

lines = text.splitlines()
i = 0
total_event = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("#EXTINF"):
        group = ""
        m = re.search(r'group-title="([^"]+)"', line)
        if m:
            group = m.group(1)
        name = line.split(",", 1)[1].strip() if "," in line else ""
        if "EVENT" in group.upper():
            total_event += 1
            print(f"{total_event}. group='{group}' | name='{name}'")
        # loncat ke EXTINF berikutnya
        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith("#EXTINF"):
            j += 1
        i = j
    else:
        i += 1
print(f"\nTOTAL EVENT: {total_event}")
