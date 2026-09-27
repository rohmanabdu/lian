import requests
import re
import os
import json

# ================== CONFIG ==================
DRIVE_FILE_ID = "1BS_-b7RJJwINV-U8p5NdNYldDW7GmfLn"
EXCLUDED_CATEGORY = "playlist koko uyo"
OUTPUT_FILE = "playlist/rama1.m3u"

# LOGO BARU KAMU - SEKARANG DIPAKSA KE SEMUA CHANNEL
DEFAULT_LOGO = "https://img.magnific.com/premium-vector/live-streaming-icon-live-broadcasting-button-online-stream-icon_349999-1413.jpg"
# ============================================

def normalize(s):
    return str(s or "").lower().strip()

def clean(s):
    return str(s or "").replace("\r", "").strip()

def is_video_url(url):
    val = str(url or "").lower().strip()
    if not val: return False
    try:
        from urllib.parse import urlparse
        path = urlparse(val).path.lower()
    except:
        path = val
    VIDEO_EXTENSIONS = [".mp4",".mkv",".avi",".mov",".webm",".flv",".wmv",".m4v",".mpeg",".mpg",".3gp"]
    for ext in VIDEO_EXTENSIONS:
        if path.endswith(ext) or ext in val:
            return True
    return False

def parse_m3u(text):
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    result = []
    current = None
    for line in lines:
        if line.startswith("#EXTINF"):
            name = line.split(",")[-1]
            group = re.search(r'group-title="([^"]*)"', line, re.I)
            category = group.group(1) if group else ""
            current = {"name": clean(name), "category": clean(category), "logo": DEFAULT_LOGO}
            continue
        if current and not line.startswith("#") and line.startswith("http"):
            result.append({
                "name": current["name"],
                "url": line,
                "category": current["category"],
                "logo": DEFAULT_LOGO # <-- PAKSA DEFAULT
            })
            current = None
    return result

def parse_txt(text):
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    result = []
    category = ""
    for line in lines:
        m = re.match(r'^\[([^\]]+)\]$', line)
        if m:
            category = clean(m.group(1)); continue
        if line.endswith(":") and "://" not in line:
            category = clean(line[:-1]); continue
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 2:
                name = clean(parts[0]); url = clean(parts[1])
                if name and url.startswith("http"):
                    result.append({"name": name, "url": url, "category": category, "logo": DEFAULT_LOGO})
    return result

def extract_json(data, result, inherited_category=""):
    if not data: return
    if isinstance(data, list):
        for item in data: extract_json(item, result, inherited_category)
        return
    if not isinstance(data, dict): return
    category = data.get("category") or data.get("group") or inherited_category or ""
    name = data.get("name") or data.get("title") or data.get("channel") or ""
    url = data.get("url") or data.get("link") or data.get("stream") or ""
    if isinstance(url, str) and url.strip() and isinstance(name, str) and name.strip():
        result.append({"name": clean(name), "url": clean(url), "category": clean(category), "logo": DEFAULT_LOGO})
        return
    for v in data.values():
        if isinstance(v, (dict, list)): extract_json(v, result, category)

def parse_playlist(text):
    text = text.strip()
    try:
        j = json.loads(text)
        res = []; extract_json(j, res, "")
        if res: return res
    except: pass
    if "#EXTM3U" in text or "#EXTINF" in text: return parse_m3u(text)
    return parse_txt(text)

def create_m3u(items):
    out = "#EXTM3U\n"
    for item in items:
        # SEMUA LOGO DIPAKSA DEFAULT_LOGO
        logo = DEFAULT_LOGO
        cat = item.get("category") or "LIVE"
        name = item.get("name") or "Channel"
        out += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{cat}",{name}\n{item["url"]}\n'
    return out

def main():
    os.makedirs("playlist", exist_ok=True)
    SOURCE_URL = f"https://drive.usercontent.google.com/download?id={DRIVE_FILE_ID}&export=download&confirm=t"
    r = requests.get(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
    r.raise_for_status()
    playlist = parse_playlist(r.text)
    filtered = [i for i in playlist if normalize(i.get("category"))!= normalize(EXCLUDED_CATEGORY) and not is_video_url(i.get("url"))]
    m3u = create_m3u(filtered)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f: f.write(m3u)
    print(f"SELESAI -> {OUTPUT_FILE} | {len(filtered)} channel | semua logo dipaksa {DEFAULT_LOGO}")

if __name__ == "__main__":
    main()
