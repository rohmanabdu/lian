name: Update Playlist Otomatis
on:
  schedule:
    - cron: '17 * * * *'
  workflow_dispatch:
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install requests
      - name: Update rama2.m3u (Google Drive)
        run: python scripts/rama2.py
      - name: Update rama1.m3u (Event)
        run: python scripts/rama1.py
      - name: Commit & Push
        run: |
          git config --global user.name "auto-bot"
          git config --global user.email "bot@github.com"
          git add playlist/
          git diff --staged --quiet || git commit -m "Auto update playlist & rama1 - $(date -u)"
          git push
