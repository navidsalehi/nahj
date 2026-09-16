"""Rebuild the static search index from existing content. Requires beautifulsoup4.
Run: python scripts/build-search.py
"""
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
records = []
def text(node):
    return node.get_text(' ', strip=True) if node else ''

for path in sorted((ROOT / 'quote').glob('*.html'), key=lambda p: int(p.stem)):
    original = path.read_text()
    soup = BeautifulSoup(original, 'html.parser')
    for i, card in enumerate(soup.select('.hikam-card')):
        number = (int(path.stem) - 1) * 20 + i + 1
        anchor = f'wisdom-{number}'
        # Stable deep links without reformatting the original documents.
        old = str(card.attrs.get('data-s', ''))
        marker = f'<article class="hikam-card" data-s="{old}">'
        original = original.replace(marker, f'<article class="hikam-card" id="{anchor}" data-s="{old}">')
        records.append(dict(kind='wisdom', number=number, url=f'quote/{path.name}#{anchor}',
            fa=text(card.select_one('.num')), en=f'Wisdom {number}',
            ar=text(card.select_one('.ar')), bodyFa=text(card.select_one('.tr.fa-only')),
            bodyEn=text(card.select_one('.tr.en-only'))))
    if original != path.read_text():
        path.write_text(original)

for path in sorted((ROOT / 'letter').glob('*.html'), key=lambda p: int(p.stem)):
    soup = BeautifulSoup(path.read_text(), 'html.parser')
    blocks = soup.select('.tr-body')
    records.append(dict(kind='letter', number=int(path.stem), url=f'letter/{path.name}',
        fa=text(soup.select_one('.letter-title.fa-only')), en=text(soup.select_one('.letter-title.en-only')),
        ar=text(soup.select_one('.ar-body')), bodyFa=text(blocks[0]) if blocks else '',
        bodyEn=text(blocks[1]) if len(blocks)>1 else ''))

soup = BeautifulSoup((ROOT/'khutbah-detail.html').read_text(), 'html.parser')
records.append(dict(kind='sermon', number=1, url='khutbah-detail.html',
    fa=text(soup.select_one('h1.fa-only')), en='Sermon 1 — The beginning of creation',
    ar=text(soup.select_one('#arText')), bodyFa=text(soup.select_one('.letter-block.fa-only .tr-body')), bodyEn=''))
(ROOT/'assets/search-index.json').write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')))
# Featured texts are copied from the library, never generated.
featured = [next(r for r in records if r['kind']=='wisdom' and r['number']==n) for n in (5,4,6,13,21)]
(ROOT/'assets/featured.json').write_text(json.dumps(featured, ensure_ascii=False, separators=(',', ':')))
print(f'Indexed {len(records)} existing texts.')
