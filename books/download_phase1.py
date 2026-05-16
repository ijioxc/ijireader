"""
批次下載 Standard Ebooks Phase 1 書單並轉成 reader JSON。
使用 venv: python3 download_phase1.py

Standard Ebooks EPUB URL 格式:
  https://standardebooks.org/ebooks/{author}/{title}/downloads/{author}_{title}.epub
"""

import urllib.request
import os
import sys
import time
from pathlib import Path

# ── 書單設定 ────────────────────────────────────────────
# (book_id, display_title, se_epub_url)
# gatsby 已完成，略過。
# 1984 / Brave New World 在 SE 上可能需要確認，列於最後。
BOOKS = [
    (
        'dorian_gray',
        'The Picture of Dorian Gray',
        'https://standardebooks.org/ebooks/oscar-wilde/the-picture-of-dorian-gray/downloads/oscar-wilde_the-picture-of-dorian-gray.epub?source=download',
    ),
    (
        'sherlock_holmes',
        'The Adventures of Sherlock Holmes',
        'https://standardebooks.org/ebooks/arthur-conan-doyle/the-adventures-of-sherlock-holmes/downloads/arthur-conan-doyle_the-adventures-of-sherlock-holmes.epub?source=download',
    ),
    (
        'frankenstein',
        'Frankenstein',
        'https://standardebooks.org/ebooks/mary-wollstonecraft-shelley/frankenstein/downloads/mary-wollstonecraft-shelley_frankenstein.epub?source=download',
    ),
    (
        'moby_dick',
        'Moby-Dick',
        'https://standardebooks.org/ebooks/herman-melville/moby-dick/downloads/herman-melville_moby-dick.epub?source=download',
    ),
    (
        'meditations',
        'Meditations',
        'https://standardebooks.org/ebooks/marcus-aurelius/meditations/george-long/downloads/marcus-aurelius_meditations_george-long.epub?source=download',
    ),
    (
        'beyond_good_and_evil',
        'Beyond Good and Evil',
        'https://standardebooks.org/ebooks/friedrich-nietzsche/beyond-good-and-evil/helen-zimmern/downloads/friedrich-nietzsche_beyond-good-and-evil_helen-zimmern.epub?source=download',
    ),
    (
        'the_republic',
        'The Republic',
        'https://standardebooks.org/ebooks/plato/the-republic/benjamin-jowett/downloads/plato_the-republic_benjamin-jowett.epub?source=download',
    ),
    (
        'the_prophet',
        'The Prophet',
        'https://standardebooks.org/ebooks/kahlil-gibran/the-prophet/downloads/kahlil-gibran_the-prophet.epub?source=download',
    ),
    (
        'monte_cristo',
        'The Count of Monte Cristo',
        'https://standardebooks.org/ebooks/alexandre-dumas/the-count-of-monte-cristo/chapman-and-hall/downloads/alexandre-dumas_the-count-of-monte-cristo_chapman-and-hall.epub?source=download',
    ),
    (
        'three_musketeers',
        'The Three Musketeers',
        'https://standardebooks.org/ebooks/alexandre-dumas/the-three-musketeers/william-robson/downloads/alexandre-dumas_the-three-musketeers_william-robson.epub?source=download',
    ),
    # 以下兩本在 SE 上需要確認版權狀態，若 404 則跳過
    (
        '1984',
        '1984',
        'https://standardebooks.org/ebooks/george-orwell/nineteen-eighty-four/downloads/george-orwell_nineteen-eighty-four.epub?source=download',
    ),
    (
        'brave_new_world',
        'Brave New World',
        'https://standardebooks.org/ebooks/aldous-huxley/brave-new-world/downloads/aldous-huxley_brave-new-world.epub?source=download',
    ),
]

EPUB_CACHE_DIR = Path(__file__).parent / '_epub_cache'
EPUB_CACHE_DIR.mkdir(exist_ok=True)

def download_epub(url: str, dest: Path) -> bool:
    if dest.exists():
        print(f'  (cached) {dest.name}')
        return True
    print(f'  Downloading {dest.name} ...', end='', flush=True)
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; epub-downloader/1.0)'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status != 200:
                print(f' HTTP {resp.status} — skipped')
                return False
            data = resp.read()
        dest.write_bytes(data)
        print(f' {len(data)//1024}KB ok')
        return True
    except Exception as e:
        print(f' ERROR: {e}')
        return False

def main():
    # 確保 epub_to_json 可 import
    sys.path.insert(0, str(Path(__file__).parent))
    from epub_to_json import convert

    ok, fail = [], []

    for book_id, title, url in BOOKS:
        book_out = Path(__file__).parent / book_id
        if (book_out / 'manifest.json').exists():
            print(f'[skip] {title} — already converted')
            continue

        print(f'\n[{title}]')
        epub_file = EPUB_CACHE_DIR / f'{book_id}.epub'

        if not download_epub(url, epub_file):
            fail.append(title)
            continue

        try:
            convert(str(epub_file), book_id, title)
            ok.append(title)
        except Exception as e:
            print(f'  CONVERT ERROR: {e}')
            fail.append(title)

        time.sleep(0.5)  # 稍微禮貌對待 SE 伺服器

    print(f'\n{"─"*50}')
    print(f'✓ 成功: {len(ok)} 本')
    for t in ok:
        print(f'    {t}')
    if fail:
        print(f'✗ 失敗: {len(fail)} 本')
        for t in fail:
            print(f'    {t}')

if __name__ == '__main__':
    main()
