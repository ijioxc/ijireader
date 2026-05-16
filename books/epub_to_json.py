"""
EPUB → reader JSON converter
Usage: python3 epub_to_json.py <epub_file> <book_id> [book_title]

Output:
  books/<book_id>/manifest.json
  books/<book_id>/chapters/0001.json ...
"""

import zipfile, json, os, re, sys
from pathlib import Path
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

NAMESPACES = {
    'opf': 'http://www.idpf.org/2007/opf',
    'dc':  'http://purl.org/dc/elements/1.1/',
    'xml': 'http://www.w3.org/XML/1998/namespace',
}

def find_opf(zf: zipfile.ZipFile) -> str:
    """Locate the OPF file via META-INF/container.xml."""
    container_xml = zf.read('META-INF/container.xml')
    root = ET.fromstring(container_xml)
    ns = {'ns': 'urn:oasis:names:tc:opendocument:xmlns:container'}
    rootfile = root.find('.//ns:rootfile', ns)
    return rootfile.attrib['full-path']

def parse_opf(zf: zipfile.ZipFile, opf_path: str):
    """Return (book_title, ordered list of (href, id)) from spine."""
    opf_dir = str(Path(opf_path).parent)
    opf_dir = '' if opf_dir == '.' else opf_dir + '/'

    raw = zf.read(opf_path)
    root = ET.fromstring(raw)

    # title
    title_el = root.find('.//dc:title', NAMESPACES)
    title = title_el.text.strip() if title_el is not None else 'Unknown'

    # id → href map from manifest
    manifest_items = {}
    for item in root.findall('.//opf:manifest/opf:item', NAMESPACES):
        manifest_items[item.attrib['id']] = {
            'href': opf_dir + item.attrib['href'],
            'media_type': item.attrib.get('media-type', ''),
        }

    # spine order
    spine = []
    for itemref in root.findall('.//opf:spine/opf:itemref', NAMESPACES):
        idref = itemref.attrib['idref']
        if idref in manifest_items:
            info = manifest_items[idref]
            if 'html' in info['media_type'] or info['href'].endswith(('.html', '.xhtml', '.htm')):
                spine.append(info['href'])

    return title, spine

def html_to_paragraphs(html_bytes: bytes) -> list[str]:
    """Extract non-empty paragraph strings from an HTML/XHTML chapter."""
    soup = BeautifulSoup(html_bytes, 'lxml')

    # Remove nav, header metadata blocks
    for tag in soup.find_all(['nav', 'header']):
        tag.decompose()

    body = soup.find('body') or soup
    paras = []

    for el in body.find_all(['p', 'blockquote', 'li']):
        text = el.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 10:   # skip very short fragments
            paras.append(text)

    return paras

def chapter_title_from_html(html_bytes: bytes, fallback: str) -> str:
    soup = BeautifulSoup(html_bytes, 'lxml')
    for tag in ['h1', 'h2', 'h3']:
        el = soup.find(tag)
        if el:
            t = el.get_text(strip=True)
            if t:
                return t
    title_el = soup.find('title')
    if title_el:
        t = title_el.get_text(strip=True)
        if t:
            return t
    return fallback

def is_frontmatter(href: str) -> bool:
    """Skip cover, TOC, title-page, copyright, colophon, etc."""
    name = Path(href).stem.lower()
    skip = {'cover', 'toc', 'titlepage', 'title-page', 'halftitlepage',
            'colophon', 'copyright', 'imprint', 'dedication', 'epigraph',
            'preface', 'introduction', 'foreword', 'acknowledgments',
            'loi', 'lot', 'index', 'appendix', 'bibliography', 'endnotes',
            'afterword', 'uncopyright', 'glossary'}
    # Also skip if the name contains any skip keyword
    return any(k in name for k in skip)

def convert(epub_path: str, book_id: str, book_title_override: str = ''):
    base_dir = Path(__file__).parent
    out_dir = base_dir / book_id
    chapters_dir = out_dir / 'chapters'
    chapters_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(epub_path) as zf:
        opf_path = find_opf(zf)
        epub_title, spine = parse_opf(zf, opf_path)
        book_title = book_title_override or epub_title

        chapter_num = 0
        manifest_chapters = []

        for href in spine:
            if is_frontmatter(href):
                continue

            try:
                html_bytes = zf.read(href)
            except KeyError:
                # try without leading path component
                alt = '/'.join(href.split('/')[1:])
                try:
                    html_bytes = zf.read(alt)
                except KeyError:
                    print(f'  WARNING: cannot read {href}, skipping')
                    continue

            paras = html_to_paragraphs(html_bytes)
            if not paras:
                continue  # skip empty/navigation pages

            chapter_num += 1
            ch_title = chapter_title_from_html(html_bytes, f'Chapter {chapter_num}')
            ch_filename = f'{chapter_num:04d}.json'

            chapter_data = {
                'id': chapter_num,
                'title': ch_title,
                'content_en': '\n\n'.join(paras),
                'content_zh': '',
            }

            with open(chapters_dir / ch_filename, 'w', encoding='utf-8') as f:
                json.dump(chapter_data, f, ensure_ascii=False, indent=2)

            manifest_chapters.append({
                'id': chapter_num,
                'title': ch_title,
                'url': f'chapters/{ch_filename}',
            })

        manifest = {
            'title': book_title,
            'chapters': manifest_chapters,
        }

        with open(out_dir / 'manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        print(f'✓ {book_title}  →  {chapter_num} chapters  [{out_dir}]')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python3 epub_to_json.py <epub_file> <book_id> [title]')
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else '')
