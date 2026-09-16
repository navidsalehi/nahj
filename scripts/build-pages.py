"""Regenerate the inner pages with the shared site chrome (topbar, footer, search
dialog) while keeping every existing text unchanged. Pure standard library.

Run: python3 scripts/build-pages.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://imamali.xyz/'

ICONS = {
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/>',
    'close': '<path d="m6 6 12 12M6 18 18 6"/>',
    'arrow': '<path d="M19 12H5m6-6-6 6 6 6"/>',
    'book': '<path d="M12 6c-3-2-6-2-10-1v14c4-1 7-1 10 1 3-2 6-2 10-1V5c-4-1-7-1-10 1Zm0 0v14"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    'star': '<path d="m12 2 2.8 7.2L22 12l-7.2 2.8L12 22l-2.8-7.2L2 12l7.2-2.8L12 2Z"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 1v2m0 18v2M1 12h2m18 0h2M4 4l2 2m12 12 2 2M4 20l2-2M18 6l2-2"/>',
    'audio': '<path d="M4 10v4h4l5 4V6l-5 4H4Zm12-1a4 4 0 0 1 0 6m2.5-9a8 8 0 0 1 0 12"/>',
    'share': '<path d="M12 15V3m-4 4 4-4 4 4M5 12v8h14v-8"/>',
    'copy': '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>',
    'print': '<path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2M6 14h12v7H6z"/>',
    'chevron': '<path d="m15 6-6 6 6 6"/>',
    'info': '<circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/>',
    'home': '<path d="m3 11 9-8 9 8v10a1 1 0 0 1-1 1h-5v-7h-6v7H4a1 1 0 0 1-1-1V11Z"/>',
}


def icon(name, extra=''):
    return (f'<svg class="icon {extra}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def bi(fa, en):
    return f'<span class="fa-only">{fa}</span><span class="en-only">{en}</span>'


def esc(s):
    return html.escape(s, quote=True)


def head(root, title, description, canonical, extra=''):
    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#0b1526"><link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="نهج البلاغه"><meta property="og:locale" content="fa_IR">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}">
<link rel="preload" href="{root}assets/fonts/vazirmatn-arabic-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}style.css"><link rel="stylesheet" href="{root}site.css">
<script src="{root}library-search.js" defer></script>
<script src="{root}site.js" defer></script>
{extra}</head>
'''


def topbar(root, active):
    def link(href, fa, en, key):
        cls = ' class="active" aria-current="page"' if key == active else ''
        return f'<li><a href="{root}{href}"{cls}>{bi(fa, en)}</a></li>'
    links = ''.join([
        link('index.html', 'خانه', 'Home', 'home'),
        link('khutbah.html', 'خطبه‌ها', 'Sermons', 'sermons'),
        link('rasail.html', 'نامه‌ها', 'Letters', 'letters'),
        link('quote/1.html', 'حکمت‌ها', 'Wisdoms', 'wisdoms'),
        link('about.html', 'درباره', 'About', 'about'),
    ])
    return f'''<a class="skip-link" href="#main">{bi('پرش به محتوا', 'Skip to content')}</a>
<div class="reading-progress" aria-hidden="true"></div>
<header class="topbar"><div class="topbar-inner">
<a class="brand" href="{root}index.html"><span class="brand-emblem" aria-hidden="true">ن</span><span class="brand-name">نهج البلاغه<small>NAHJ AL-BALAGHA</small></span></a>
<nav aria-label="ناوبری اصلی" data-label-fa="ناوبری اصلی" data-label-en="Main navigation"><ul class="nav-links" id="primary-nav">{links}</ul></nav>
<div class="header-tools"><button class="icon-button" id="open-search" type="button" aria-label="جستجو" data-label-fa="جستجو" data-label-en="Search">{icon('search')}</button>
<div class="lang-switch" role="group" aria-label="Language"><button type="button" class="on" data-lang="fa" aria-pressed="true">FA</button><button type="button" data-lang="en" aria-pressed="false">EN</button></div>
<button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="منو" data-label-fa="منو" data-label-en="Menu"><span class="menu-btn-icon" aria-hidden="true"></span></button></div>
</div></header>
'''


def footer(root):
    return f'''<footer class="home-footer"><div class="home-wrap"><div class="footer-top"><a class="brand" href="{root}index.html"><span class="brand-emblem" aria-hidden="true">ن</span><span class="brand-name">نهج البلاغه<small>THE PATH OF ELOQUENCE</small></span></a><p>{bi('سخن ماندگار، برای زندگی امروز.', 'Timeless words, for life today.')}</p><a href="{root}about.html">{bi('درباره این مجموعه', 'About this project')}{icon('arrow', 'directional')}</a></div><div class="footer-bottom"><span>imamali.xyz</span><span>{bi('برای همه، همیشه رایگان', 'Open to everyone. Always free.')}</span><a href="#main">{bi('بازگشت به بالا', 'Back to top')}<span aria-hidden="true">↑</span></a></div></div></footer>
<dialog class="search-dialog" id="search-dialog" aria-labelledby="search-title"><div class="dialog-header"><h2 id="search-title">{bi('جستجو در نهج البلاغه', 'Search the collection')}</h2><button type="button" class="icon-button" id="close-search" aria-label="بستن" data-label-fa="بستن" data-label-en="Close">{icon('close')}</button></div><form action="{root}search.html" class="quick-search-form" role="search"><label class="visually-hidden" for="quick-query">{bi('کلمه یا موضوع', 'Word or topic')}</label>{icon('search')}<input id="quick-query" name="q" type="search" placeholder="کلمه یا موضوعی بنویسید…" data-placeholder-fa="کلمه یا موضوعی بنویسید…" data-placeholder-en="Search a word or topic…" autocomplete="off"><button class="gold-button" type="submit">{bi('جستجو', 'Search')}</button></form><p id="quick-status" role="status">{bi('در خطبه‌ها، نامه‌ها و حکمت‌های موجود جستجو کنید.', 'Search the available sermons, letters, and wisdoms.')}</p><div id="quick-results"></div><div class="dialog-footer">{bi('برای بستن، Escape را بزنید', 'Press Escape to close')}<kbd>ESC</kbd></div></dialog>
<div class="toast" id="toast" role="status"></div>
'''


END = '</body></html>\n'


def page_head(eyebrow_icon, eyebrow, title, lede, facts=(), crumbs=(), links=()):
    facts_html = ''.join(f'<span><strong>{v}</strong>{k}</span>' for k, v in facts)
    crumb_items = ''.join(
        (f'<li><a href="{href}">{label}</a></li>' if href else f'<li aria-current="page">{label}</li>')
        for label, href in crumbs)
    links_html = ''.join(f'<a href="{href}">{label}{icon("arrow", "directional")}</a>' for label, href in links)
    nav = ''
    if crumbs or links:
        nav = (f'<div class="page-head-nav"><div class="home-wrap"><nav class="breadcrumb" aria-label="مسیر" data-label-fa="مسیر" data-label-en="Breadcrumb">'
               f'<ol>{crumb_items}</ol></nav><div class="head-links">{links_html}</div></div></div>')
    return f'''<section class="page-head"><div class="home-wrap page-head-inner"><div>
<p class="eyebrow">{icon(eyebrow_icon)}{eyebrow}</p>
<h1>{title}</h1>
<p class="page-lede">{lede}</p></div>
{f'<div class="page-facts">{facts_html}</div>' if facts_html else ''}</div>{nav}</section>
'''


def write(path, content):
    if not content.rstrip().endswith('</html>'):
        content = content.rstrip('\n') + '\n' + END
    (ROOT / path).write_text(content, encoding='utf-8')
    print('wrote', path)


# ---------------------------------------------------------------- sermons
SERMONS = [
    (1, 'آغاز آفرینش', 'On the beginning of creation', 'در توحید و معاد و آفرینش آسمان و زمین',
     'On unity, the return, and the creation of the heavens and earth', 'khutbah-detail.html'),
    (2, 'پس از بازگشت از صفین', 'After returning from Siffin', 'گواهی به توحید و رسالت و وصف جاهلیت',
     'Testimony of unity and prophethood, and a description of the Age of Ignorance', None),
    (3, 'شقشقیه', 'Ash-Shaqshaqiya', 'شکوه از غصب خلافت — معروف‌ترین خطبه',
     'Complaint about the usurpation of the caliphate — the best-known sermon', None),
    (27, 'جهاد', 'On jihad', 'تشویق به جهاد و نکوهش سستی', 'Urging struggle and reproaching slackness', None),
    (193, 'متقین (همام)', 'The God-fearing (Hammam)', 'توصیف ویژگی‌های پرهیزگاران',
     'Description of the qualities of the God-fearing', None),
    (234, 'توحید (اشباح)', 'On divine unity (al-Ashbah)', 'از خطبه‌های جلیل در صفات خداوند',
     'Among the great sermons on the attributes of God', None),
]


def build_khutbah():
    cards = []
    for n, fa, en, dfa, den, href in SERMONS:
        num = bi(f'خطبه {n}', f'Sermon {n}')
        if href:
            cards.append(f'''<a class="entry" href="{href}" data-s="{n} {esc(fa)} {esc(en)}"><div class="entry-top"><span class="entry-num">{num}</span><span class="entry-tag">{bi('متن موجود', 'Text available')}</span></div><h2>{bi(esc(fa), esc(en))}</h2><p>{bi(esc(dfa), esc(den))}</p><div class="entry-bottom"><span>{bi('عربی · فارسی', 'Arabic · Persian')}</span><span class="round-arrow">{icon('arrow', 'directional')}</span></div></a>''')
        else:
            cards.append(f'''<article class="entry pending" data-s="{n} {esc(fa)} {esc(en)}"><div class="entry-top"><span class="entry-num">{num}</span><span class="entry-tag">{bi('به‌زودی', 'Coming soon')}</span></div><h2>{bi(esc(fa), esc(en))}</h2><p>{bi(esc(dfa), esc(den))}</p><div class="entry-bottom"><span>{bi('متن کامل هنوز اضافه نشده', 'Full text not yet added')}</span><span class="round-arrow">{icon('arrow', 'directional')}</span></div></article>''')
    body = f'''<body class="lang-fa site">
{topbar('', 'sermons')}
<main id="main">
{page_head('book', bi('بخش نخست', 'Part one'), bi('خطبه‌ها', 'Sermons'),
           bi('سخنان بلیغ امیرالمؤمنین علی علیه‌السلام درباره توحید، آفرینش، عدالت و انسان. در این مرحله فهرست گزیده‌ای از خطبه‌ها آماده است و متن کامل به‌تدریج اضافه می‌شود.',
              'Eloquent addresses of Imam Ali (AS) on divine unity, creation, justice, and the human condition. A selected list is ready at this stage; full texts are being added gradually.'),
           facts=[(bi('در فهرست', 'listed'), bi('۶', '6')), (bi('متن موجود', 'with text'), bi('۱', '1')), (bi('در کتاب', 'in the book'), bi('۲۴۱', '241'))],
           crumbs=[(bi('خانه', 'Home'), 'index.html'), (bi('خطبه‌ها', 'Sermons'), None)],
           links=[(bi('جستجو در همه متن‌ها', 'Search all texts'), 'search.html?kind=sermon')])}
<section class="home-wrap page-body" aria-labelledby="list-title">
<h2 id="list-title" class="visually-hidden">{bi('فهرست خطبه‌ها', 'List of sermons')}</h2>
<div class="list-tools"><label class="filter-field"><span class="visually-hidden">{bi('فیلتر خطبه‌ها', 'Filter sermons')}</span>{icon('search')}<input id="filter" type="search" placeholder="فیلتر بر اساس شماره یا موضوع…" data-placeholder-fa="فیلتر بر اساس شماره یا موضوع…" data-placeholder-en="Filter by number or topic…" autocomplete="off"></label><p class="list-status" id="list-status" role="status" data-default-fa="۶ خطبه در فهرست · ۱ متن کامل" data-default-en="6 sermons listed · 1 full text"></p></div>
<div class="entry-grid" id="list">{''.join(cards)}</div>
<p class="empty-note" id="list-empty" hidden>{bi('خطبه‌ای با این مشخصات پیدا نشد. می‌توانید در <a href="search.html">جستجوی کامل</a> امتحان کنید.', 'No sermon matches. Try the <a href="search.html">full search</a> instead.')}</p>
</section>
</main>
{footer('')}'''
    write('khutbah.html', head('', 'خطبه‌های نهج البلاغه | سخنرانی‌های امام علی علیه‌السلام',
                               'فهرست و متن خطبه‌های نهج البلاغه — سخنرانی‌ها و مواعظ امیرالمؤمنین علی علیه‌السلام با ترجمه فارسی.',
                               SITE + 'khutbah.html') + body)


# ---------------------------------------------------------------- letters
def build_rasail():
    letters = json.loads((ROOT / 'assets/letters.json').read_text(encoding='utf-8'))
    assert len(letters) == 79, len(letters)
    available = {int(p.stem) for p in (ROOT / 'letter').glob('*.html')}
    cards = []
    for item in letters:
        n, fa_h, en_h, fa_p, ds = item['n'], item['fa'], item['en'], item['note'], item['s']
        num = bi(f'نامه {n}', f'Letter {n}')
        # The short context line only exists in Persian; show it once, in either language.
        desc = f'<p>{esc(fa_p)}</p>'
        if n in available:
            cards.append(f'''<a class="entry" href="letter/{n}.html" data-s="{esc(ds)} {esc(en_h)}"><div class="entry-top"><span class="entry-num">{num}</span><span class="entry-tag">{bi('متن کامل', 'Full text')}</span></div><h2 class="fa-only">{fa_h}</h2><h2 class="en-only">{en_h}</h2>{desc}<div class="entry-bottom"><span>{bi('عربی · فارسی · انگلیسی', 'Arabic · Persian · English')}</span><span class="round-arrow">{icon('arrow', 'directional')}</span></div></a>''')
        else:
            cards.append(f'''<article class="entry pending" data-s="{esc(ds)} {esc(en_h)}"><div class="entry-top"><span class="entry-num">{num}</span><span class="entry-tag">{bi('به‌زودی', 'Coming soon')}</span></div><h2 class="fa-only">{fa_h}</h2><h2 class="en-only">{en_h}</h2>{desc}<div class="entry-bottom"><span>{bi('متن کامل هنوز اضافه نشده', 'Full text not yet added')}</span><span class="round-arrow">{icon('arrow', 'directional')}</span></div></article>''')
    avail = len(available)
    body = f'''<body class="lang-fa site">
{topbar('', 'letters')}
<main id="main">
{page_head('mail', bi('بخش دوم', 'Part two'), bi('نامه‌ها', 'Letters'),
           bi('۷۹ نامه و عهدنامه امیرالمؤمنین به کارگزاران، فرماندهان، فرزندان و مخالفان؛ از اندرزهای پدرانه تا آیین حکومت‌داری. متن کامل نامه‌های ۱ تا ۲۰ آماده است و بقیه به‌تدریج اضافه می‌شود.',
              '79 letters and covenants of Imam Ali (AS) to governors, commanders, his children, and opponents — from fatherly counsel to the principles of statecraft. Letters 1–20 have full text; the rest follow gradually.'),
           facts=[(bi('در کتاب', 'in the book'), bi('۷۹', '79')), (bi('متن کامل', 'full text'), bi(str(avail).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')), str(avail)))],
           crumbs=[(bi('خانه', 'Home'), 'index.html'), (bi('نامه‌ها', 'Letters'), None)],
           links=[(bi('عهدنامه مالک اشتر', 'Covenant to Malik al-Ashtar'), 'rasail-detail.html'), (bi('جستجو در همه متن‌ها', 'Search all texts'), 'search.html?kind=letter')])}
<section class="home-wrap page-body" aria-labelledby="list-title">
<h2 id="list-title" class="visually-hidden">{bi('فهرست نامه‌ها', 'List of letters')}</h2>
<div class="list-tools"><label class="filter-field"><span class="visually-hidden">{bi('فیلتر نامه‌ها', 'Filter letters')}</span>{icon('search')}<input id="filter" type="search" placeholder="فیلتر بر اساس شماره، مخاطب یا موضوع…" data-placeholder-fa="فیلتر بر اساس شماره، مخاطب یا موضوع…" data-placeholder-en="Filter by number, recipient, or topic…" autocomplete="off"></label><div class="chip-row" role="group" aria-label="نمایش" data-label-fa="نمایش" data-label-en="Show"><button type="button" data-show="all" aria-pressed="true">{bi('همه', 'All')}</button><button type="button" data-show="available" aria-pressed="false">{bi('فقط متن کامل', 'Full text only')}</button></div></div>
<p class="list-status" id="list-status" role="status" data-default-fa="۷۹ نامه · {avail} متن کامل" data-default-en="79 letters · {avail} with full text"></p>
<div class="entry-grid" id="list">{''.join(cards)}</div>
<p class="empty-note" id="list-empty" hidden>{bi('نامه‌ای با این مشخصات پیدا نشد. می‌توانید در <a href="search.html">جستجوی کامل</a> امتحان کنید.', 'No letter matches. Try the <a href="search.html">full search</a> instead.')}</p>
</section>
</main>
{footer('')}
<script>
(function(){{
  var list=document.getElementById('list'),chips=document.querySelectorAll('[data-show]');
  chips.forEach(function(c){{c.addEventListener('click',function(){{
    chips.forEach(function(x){{x.setAttribute('aria-pressed',String(x===c));}});
    list.classList.toggle('only-available',c.dataset.show==='available');
  }});}});
}})();
</script>
</body></html>'''
    extra_css = '<style>#list.only-available .entry.pending{display:none}</style>\n'
    write('rasail.html', head('', 'نامه‌های نهج البلاغه | مکاتبات امام علی علیه‌السلام',
                              'فهرست نامه‌ها و عهدنامه‌های نهج البلاغه با ترجمه فارسی و انگلیسی — از جمله عهدنامه مالک اشتر.',
                              SITE + 'rasail.html', extra_css) + body)


# ---------------------------------------------------------------- wisdom pages
def build_quotes():
    fa_digits = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    for path in sorted((ROOT / 'quote').glob('*.html'), key=lambda p: int(p.stem)):
        n = int(path.stem)
        src = path.read_text(encoding='utf-8')
        m = re.search(r'<div class="hikam-grid" id="list">(.*?)</div>\s*(?:<nav class="pagination"|<p class="empty-note")', src, re.S)
        if not m:
            m = re.search(r'<div class="hikam-grid" id="list">(.*?)\n\s*</div>\s*\n', src, re.S)
        cards_html = m.group(1)
        cards = re.findall(r'<article class="hikam-card".*?</article>', cards_html, re.S)
        assert len(cards) == 20, (path, len(cards))
        # Strip any previously injected buttons; site.js adds them at runtime.
        cards = [re.sub(r'\s*<div class="card-actions">.*?</div>', '', c, flags=re.S) for c in cards]
        ld = re.search(r'<script type="application/ld\+json">.*?</script>', src, re.S).group(0)
        first, last = (n - 1) * 20 + 1, n * 20
        title = f'حکمت {first} تا {last} نهج البلاغه | کلمات قصار امام علی (صفحه {n})'
        desc = f'متن عربی و ترجمه فارسی حکمت‌های {first} تا {last} نهج البلاغه — کلمات قصار امیرالمؤمنین علی علیه‌السلام. صفحه {n} از ۲۴.'
        rel = ''
        if n > 1: rel += f'<link rel="prev" href="{SITE}quote/{n-1}.html">\n'
        if n < 24: rel += f'<link rel="next" href="{SITE}quote/{n+1}.html">\n'
        nums = ''
        for p in range(1, 25):
            cls = 'page-num' + (' on' if p == n else '') + (' near' if abs(p - n) <= 1 or p in (1, 24) else '')
            cur = ' aria-current="page"' if p == n else ''
            nums += f'<a class="{cls}" href="{p}.html"{cur}>{p}</a>'
        prev_l = (f'<a class="page-btn" href="{n-1}.html" data-nav="prev" rel="prev">{icon("arrow", "directional")}{bi("صفحه قبل", "Previous")}</a>' if n > 1
                  else f'<span class="page-btn">{icon("arrow", "directional")}{bi("صفحه قبل", "Previous")}</span>')
        next_l = (f'<a class="page-btn" href="{n+1}.html" data-nav="next" rel="next">{bi("صفحه بعد", "Next")}<svg class="icon directional" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="transform:scaleX(-1)"><path d="M19 12H5m6-6-6 6 6 6"/></svg></a>' if n < 24
                  else f'<span class="page-btn">{bi("صفحه بعد", "Next")}</span>')
        fa_first, fa_last, fa_n = str(first).translate(fa_digits), str(last).translate(fa_digits), str(n).translate(fa_digits)
        body = f'''<body class="lang-fa site" data-root="../">
{topbar('../', 'wisdoms')}
<main id="main">
{page_head('sun', bi('بخش سوم', 'Part three'), bi('کلمات قصار', 'Short sayings'),
           bi(f'حکمت {fa_first} تا {fa_last} از ۴۸۰ حکمت نهج البلاغه؛ متن عربی با ترجمه فارسی و انگلیسی. هر حکمت را می‌توانید بشنوید یا به اشتراک بگذارید.',
              f'Wisdoms {first}–{last} of the 480 short sayings of Nahj al-Balagha: the Arabic text with Persian and English translations. Each saying can be listened to or shared.'),
           facts=[(bi('صفحه', 'page'), bi(f'{fa_n} / ۲۴', f'{n} / 24')), (bi('حکمت', 'wisdoms'), bi(f'{fa_first}–{fa_last}', f'{first}–{last}')), (bi('در کتاب', 'in the book'), bi('۴۸۰', '480'))],
           crumbs=[(bi('خانه', 'Home'), '../index.html'), (bi('کلمات قصار', 'Short sayings'), '1.html' if n != 1 else None)] + ([(bi(f'صفحه {fa_n}', f'Page {n}'), None)] if n != 1 else []),
           links=[(bi('جستجو در حکمت‌ها', 'Search the wisdoms'), '../search.html?kind=wisdom')])}
<section class="home-wrap page-body" aria-labelledby="list-title">
<h2 id="list-title" class="visually-hidden">{bi(f'حکمت {fa_first} تا {fa_last}', f'Wisdoms {first} to {last}')}</h2>
<div class="list-tools"><label class="filter-field"><span class="visually-hidden">{bi('فیلتر در این صفحه', 'Filter this page')}</span>{icon('search')}<input id="filter" type="search" placeholder="فیلتر در این صفحه…" data-placeholder-fa="فیلتر در این صفحه…" data-placeholder-en="Filter this page…" autocomplete="off"></label><form class="jump-form" id="jump-form"><label for="jump">{bi('رفتن به حکمت', 'Go to wisdom')}</label><input id="jump" type="text" inputmode="numeric" placeholder="۱–۴۸۰" data-placeholder-fa="۱–۴۸۰" data-placeholder-en="1–480" autocomplete="off"><button type="submit">{bi('برو', 'Go')}</button></form></div>
<p class="list-status" id="list-status" role="status" data-default-fa="۲۰ حکمت در این صفحه" data-default-en="20 wisdoms on this page"></p>
<div class="hikam-grid" id="list">
{chr(10).join(cards)}
</div>
<p class="empty-note" id="list-empty" hidden>{bi('در این صفحه چیزی پیدا نشد. <a href="../search.html">در همه حکمت‌ها جستجو کنید</a>.', 'Nothing on this page matches. <a href="../search.html">Search all wisdoms</a>.')}</p>
<nav class="pagination" aria-label="صفحه‌بندی" data-label-fa="صفحه‌بندی" data-label-en="Pagination">
{prev_l}
<div class="page-numbers">{nums}</div>
{next_l}
<span class="page-info">{bi(f'صفحه {fa_n} از ۲۴ · حکمت {fa_first}–{fa_last}', f'Page {n} of 24 · wisdoms {first}–{last}')}</span>
</nav>
</section>
</main>
{footer('../')}'''
        write(f'quote/{n}.html', head('../', title, desc, f'{SITE}quote/{n}.html', rel + ld + '\n') + body)


# ---------------------------------------------------------------- letter pages
def build_letters():
    fa_digits = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    paths = sorted((ROOT / 'letter').glob('*.html'), key=lambda p: int(p.stem))
    available = {int(p.stem) for p in paths}
    for path in paths:
        n = int(path.stem)
        src = path.read_text(encoding='utf-8')
        title_fa = re.search(r'<h1 class="letter-title fa-only">(.*?)</h1>', src, re.S).group(1).strip()
        title_en = re.search(r'<h1 class="letter-title en-only">(.*?)</h1>', src, re.S).group(1).strip()
        ctx_fa = re.search(r'<(?:div|p) class="letter-context fa-only">(.*?)</(?:div|p)>', src, re.S).group(1).strip()
        ctx_en = re.search(r'<(?:div|p) class="letter-context en-only">(.*?)</(?:div|p)>', src, re.S).group(1).strip()
        blocks = re.findall(r'<section class="letter-block[^"]*">.*?</section>', src, re.S)
        assert len(blocks) == 3, path
        desc = re.search(r'<meta name="description" content="([^"]*)">', src).group(1)
        doc_title = re.search(r'<title>(.*?)</title>', src, re.S).group(1)
        prev_l = (f'<a href="{n-1}.html" data-nav="prev" rel="prev">{icon("arrow", "directional")}{bi(f"نامه {n-1}", f"Letter {n-1}")}</a>' if n - 1 in available
                  else f'<span class="disabled">{icon("arrow", "directional")}{bi("نامه قبل", "Previous")}</span>')
        next_l = (f'<a href="{n+1}.html" data-nav="next" rel="next">{bi(f"نامه {n+1}", f"Letter {n+1}")}<svg class="icon directional" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="transform:scaleX(-1)"><path d="M19 12H5m6-6-6 6 6 6"/></svg></a>' if n + 1 in available
                  else f'<span class="disabled">{bi("نامه بعد", "Next")}</span>')
        note_fa = 'متن کامل نامه‌های بعدی به‌تدریج اضافه می‌شود. فهرست همه ۷۹ نامه در <a href="../rasail.html">صفحه نامه‌ها</a> در دسترس است.'
        note_en = 'Full texts of the following letters are being added gradually. All 79 letters are listed on the <a href="../rasail.html">letters page</a>.'
        note = '' if n + 1 in available else '<p class="reader-note">' + bi(note_fa, note_en) + '</p>'
        fa_n = str(n).translate(fa_digits)
        rel = ''
        if n - 1 in available: rel += f'<link rel="prev" href="{SITE}letter/{n-1}.html">\n'
        if n + 1 in available: rel += f'<link rel="next" href="{SITE}letter/{n+1}.html">\n'
        ld = json.dumps({
            '@context': 'https://schema.org', '@type': 'Article',
            'headline': title_fa, 'alternativeHeadline': title_en, 'inLanguage': ['ar', 'fa', 'en'],
            'url': f'{SITE}letter/{n}.html', 'isPartOf': {'@type': 'Book', 'name': 'نهج البلاغه', 'author': {'@type': 'Person', 'name': 'علی بن ابی طالب'}},
            'author': {'@type': 'Person', 'name': 'علی بن ابی طالب', 'alternateName': 'Imam Ali'},
        }, ensure_ascii=False)
        body = f'''<body class="lang-fa site" data-root="../">
{topbar('../', 'letters')}
<main id="main">
<section class="reader-head"><div class="reader-head-inner">
<p class="eyebrow">{icon('mail')}{bi(f'نامه {fa_n} از ۷۹', f'Letter {n} of 79')}</p>
<h1 class="letter-title fa-only">{title_fa}</h1>
<h1 class="letter-title en-only">{title_en}</h1>
<p class="letter-context fa-only">{ctx_fa}</p>
<p class="letter-context en-only">{ctx_en}</p>
</div></section>
<div class="reader-tools"><div class="reader-tools-inner">
<nav class="reader-crumb" aria-label="مسیر" data-label-fa="مسیر" data-label-en="Breadcrumb"><a href="../index.html">{bi('خانه', 'Home')}</a>{icon('chevron', 'directional')}<a href="../rasail.html">{bi('نامه‌ها', 'Letters')}</a>{icon('chevron', 'directional')}<span aria-current="page">{bi(f'نامه {fa_n}', f'Letter {n}')}</span></nav>
<div class="letter-tools"><button type="button" id="btnAudio">{icon('audio')}{bi('شنیدن عربی', 'Listen (Arabic)')}</button><button type="button" id="btnCopy">{icon('copy')}{bi('کپی متن', 'Copy text')}</button><button type="button" id="btnShare">{icon('share')}{bi('اشتراک', 'Share')}</button><button type="button" id="btnPrint">{icon('print')}{bi('چاپ', 'Print')}</button></div>
</div></div>
<article class="reader-body">
{chr(10).join(blocks)}
{note}
<nav class="letter-nav" aria-label="پیمایش نامه‌ها" data-label-fa="پیمایش نامه‌ها" data-label-en="Letter navigation">
{prev_l}
<a href="../rasail.html" class="primary">{bi('همه نامه‌ها', 'All letters')}</a>
{next_l}
</nav>
</article>
</main>
{footer('../')}'''
        extra = rel + f'<script type="application/ld+json">{ld}</script>\n'
        write(f'letter/{n}.html', head('../', doc_title, desc, f'{SITE}letter/{n}.html', extra) + body)


# ---------------------------------------------------------------- sermon 1 / letter 53 excerpts
def build_excerpt(filename, kind, num_fa, num_en, title_fa, title_en, ctx_fa, ctx_en, ar, fa, meta, back_href, back_fa, back_en, ld_name, title_tag, desc, note_fa, note_en, related):
    crumb_fa, crumb_en = ('خطبه‌ها', 'Sermons') if kind == 'sermon' else ('نامه‌ها', 'Letters')
    facts = ''.join(f'<div class="side-row"><dt>{bi(k_fa, k_en)}</dt><dd>{bi(v_fa, v_en)}</dd></div>' for k_fa, k_en, v_fa, v_en in meta)
    related_html = ''.join(f'<li>{bi(r_fa, r_en)}</li>' for r_fa, r_en in related)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'Article', 'headline': title_fa, 'alternativeHeadline': title_en,
                     'inLanguage': ['ar', 'fa'], 'url': SITE + filename,
                     'isPartOf': {'@type': 'Book', 'name': 'نهج البلاغه', 'author': {'@type': 'Person', 'name': 'علی بن ابی طالب'}}}, ensure_ascii=False)
    body = f'''<body class="lang-fa site">
{topbar('', 'sermons' if kind == 'sermon' else 'letters')}
<main id="main">
<section class="reader-head"><div class="reader-head-inner">
<p class="eyebrow">{icon('book' if kind == 'sermon' else 'mail')}{bi(num_fa, num_en)}</p>
<h1 class="letter-title fa-only">{title_fa}</h1>
<h1 class="letter-title en-only">{title_en}</h1>
<p class="letter-context fa-only">{ctx_fa}</p>
<p class="letter-context en-only">{ctx_en}</p>
</div></section>
<div class="reader-tools"><div class="reader-tools-inner">
<nav class="reader-crumb" aria-label="مسیر" data-label-fa="مسیر" data-label-en="Breadcrumb"><a href="index.html">{bi('خانه', 'Home')}</a>{icon('chevron', 'directional')}<a href="{back_href}">{bi(crumb_fa, crumb_en)}</a>{icon('chevron', 'directional')}<span aria-current="page">{bi(num_fa, num_en)}</span></nav>
<div class="letter-tools"><button type="button" id="btnAudio">{icon('audio')}{bi('شنیدن عربی', 'Listen (Arabic)')}</button><button type="button" id="btnCopy">{icon('copy')}{bi('کپی متن', 'Copy text')}</button><button type="button" id="btnShare">{icon('share')}{bi('اشتراک', 'Share')}</button><button type="button" id="btnPrint">{icon('print')}{bi('چاپ', 'Print')}</button></div>
</div></div>
<article class="reader-body">
<p class="reader-note">{bi(note_fa, note_en)}</p>
<section class="letter-block">
<div class="label fa-only">متن عربی</div><div class="label en-only">Arabic</div>
<div class="ar-body" id="arText">{ar}</div>
</section>
<section class="letter-block fa-only">
<div class="label">ترجمه فارسی</div>
<div class="tr-body">{fa}</div>
</section>
<section class="letter-block en-only">
<div class="label">English</div>
<p class="tr-body en" style="color:#6b7078">An English translation of this passage has not been added yet. The Arabic text is shown above; switch to FA for the Persian translation.</p>
</section>
<section class="letter-block">
<div class="label fa-only">اطلاعات</div><div class="label en-only">Details</div>
<dl class="fact-card" style="border:0;padding:0;background:none">{facts}</dl>
</section>
<section class="letter-block">
<div class="label fa-only">مرتبط</div><div class="label en-only">Related</div>
<ul class="related-list">{related_html}</ul>
</section>
<nav class="letter-nav" aria-label="پیمایش" data-label-fa="پیمایش" data-label-en="Navigation">
<a href="{back_href}" class="primary">{icon('arrow', 'directional')}{bi(back_fa, back_en)}</a>
</nav>
</article>
</main>
{footer('')}'''
    extra = (f'<script type="application/ld+json">{ld}</script>\n'
             '<style>.fact-card .side-row{display:flex;justify-content:space-between;gap:16px;padding:10px 0;border-bottom:1px solid #ece9e0}.fact-card .side-row:last-child{border:0}.fact-card dd{margin:0;text-align:end}.related-list{display:grid;gap:8px;font-size:14px;color:#3d4654}.related-list li{display:flex;gap:10px;align-items:baseline}.related-list li:before{content:"";width:6px;height:6px;border-radius:50%;background:var(--gold);flex:none;transform:translateY(-2px)}</style>\n')
    write(filename, head('', title_tag, desc, SITE + filename, extra) + body)


def build_excerpts():
    src = (ROOT / 'khutbah-detail.html').read_text(encoding='utf-8')
    ar = re.search(r'id="arText">(.*?)</div>', src, re.S) or re.search(r'<div class="ar-text">\s*(.*?)\s*</div>', src, re.S)
    fa = re.search(r'<div class="tr-body">(.*?)</div>', src, re.S) or re.search(r'<div class="fa-text fa-only">\s*(.*?)\s*</div>', src, re.S)
    build_excerpt('khutbah-detail.html', 'sermon', 'خطبه ۱', 'Sermon 1', 'خطبه ۱ — آغاز آفرینش', 'Sermon 1 — The beginning of creation',
                  'در توحید و معاد و آفرینش آسمان و زمین. موضوع: توحید · آفرینش · معاد.',
                  'On divine unity, the return, and the creation of the heavens and earth.',
                  ar.group(1).strip(), fa.group(1).strip(),
                  [('شماره', 'Number', '۱', '1'), ('موضوع', 'Subject', 'توحید و معاد', 'Unity and the return'), ('مخاطب', 'Audience', 'عموم مردم', 'General public'), ('زبان اصلی', 'Original language', 'عربی', 'Arabic')],
                  'khutbah.html', 'همه خطبه‌ها', 'All sermons', 'خطبه ۱',
                  'خطبه ۱ نهج البلاغه — آغاز آفرینش | متن عربی و ترجمه فارسی', 'آغاز خطبه اول نهج البلاغه در توحید و آفرینش، با متن عربی و ترجمه فارسی.',
                  'این صفحه آغاز خطبه را نمایش می‌دهد؛ متن کامل خطبه به‌تدریج اضافه می‌شود.',
                  'This page shows the opening of the sermon; the full text is being added gradually.',
                  [('خطبه ۲ — پس از صفین', 'Sermon 2 — After Siffin'), ('خطبه ۳ — شقشقیه', 'Sermon 3 — Ash-Shaqshaqiya'), ('خطبه ۲۳۴ — توحید (اشباح)', 'Sermon 234 — On divine unity')])

    src = (ROOT / 'rasail-detail.html').read_text(encoding='utf-8')
    ar = re.search(r'id="arText">(.*?)</div>', src, re.S) or re.search(r'<div class="ar-text">\s*(.*?)\s*</div>', src, re.S)
    fa = re.search(r'<div class="tr-body">(.*?)</div>', src, re.S) or re.search(r'<div class="fa-text fa-only">\s*(.*?)\s*</div>', src, re.S)
    build_excerpt('rasail-detail.html', 'letter', 'نامه ۵۳', 'Letter 53', 'عهدنامه مالک اشتر', 'Covenant to Malik al-Ashtar',
                  'به مالک اشتر هنگام گماردن او بر مصر — در حکمرانی و عدالت. مخاطب: مالک اشتر · موضوع: حکومت و عدالت.',
                  'To Malik al-Ashtar on appointing him governor of Egypt — on governance and justice.',
                  ar.group(1).strip(), fa.group(1).strip(),
                  [('شماره', 'Number', '۵۳', '53'), ('مخاطب', 'Recipient', 'مالک اشتر', 'Malik al-Ashtar'), ('موضوع', 'Subject', 'حکمرانی و عدالت', 'Governance and justice'), ('زمان', 'Date', 'حدود ۳۷ هـ', 'c. 37 AH')],
                  'rasail.html', 'همه نامه‌ها', 'All letters', 'نامه ۵۳',
                  'نامه ۵۳ نهج البلاغه — عهدنامه مالک اشتر | متن عربی و ترجمه فارسی', 'گزیده‌ای از عهدنامه مالک اشتر، نامه ۵۳ نهج البلاغه در حکمرانی و عدالت، با متن عربی و ترجمه فارسی.',
                  'این صفحه گزیده‌ای از عهدنامه را نمایش می‌دهد؛ متن کامل به‌تدریج اضافه می‌شود.',
                  'This page shows an excerpt of the covenant; the full text is being added gradually.',
                  [('نامه ۲۷ — به محمد بن ابی‌بکر', 'Letter 27 — To Muhammad ibn Abi Bakr'), ('نامه ۳۱ — به امام حسن', 'Letter 31 — To Imam Hasan'), ('نامه ۴۵ — به عثمان بن حنیف', 'Letter 45 — To Uthman ibn Hunayf')])


# ---------------------------------------------------------------- about
def build_about():
    body = f'''<body class="lang-fa site">
{topbar('', 'about')}
<main id="main">
{page_head('info', bi('درباره', 'About'), bi('درباره <em>نهج البلاغه</em>', 'About <em>Nahj al-Balagha</em>'),
           bi('«راه بلاغت»؛ گزیده‌ای از خطبه‌ها، نامه‌ها و سخنان کوتاه امیرالمؤمنین علی بن ابی‌طالب علیه‌السلام که سید رضی در قرن چهارم هجری گردآوری کرد.',
              '“The path of eloquence”: a selection of the sermons, letters, and short sayings of Imam Ali ibn Abi Talib, compiled by al-Sharif al-Radi in the 4th century AH.'),
           facts=[(bi('خطبه', 'sermons'), bi('۲۴۱', '241')), (bi('نامه', 'letters'), bi('۷۹', '79')), (bi('حکمت', 'sayings'), bi('۴۸۰', '480'))],
           crumbs=[(bi('خانه', 'Home'), 'index.html'), (bi('درباره', 'About'), None)])}
<section class="home-wrap page-body about-layout">
<article class="prose">
<div class="fa-only">
<p>نهج‌البلاغه به معنای «راه بلاغت» است؛ گزیده‌ای از خطبه‌ها، نامه‌ها و سخنان کوتاه امیرالمؤمنین علی بن ابی‌طالب علیه‌السلام که <strong>سید رضی</strong> در قرن چهارم هجری گردآوری کرده است.</p>
<h2>سه بخش اصلی</h2>
<ul>
<li><strong>خطبه‌ها</strong> — حدود ۲۴۱ خطبه</li>
<li><strong>نامه‌ها</strong> — حدود ۷۹ نامه و عهدنامه</li>
<li><strong>کلمات قصار</strong> — حدود ۴۸۰ حکمت</li>
</ul>
<p>این کتاب پس از قرآن کریم از مهم‌ترین آثار ادبی و فکری جهان اسلام است و به بیش از بیست زبان ترجمه شده است.</p>
<h2>درباره این سایت</h2>
<p>imamali.xyz یک سایت ایستا، رایگان و بدون ثبت‌نام است. متن عربی همراه با ترجمه فارسی و انگلیسی نمایش داده می‌شود و ساختار کتاب — خطبه، نامه، حکمت — همان‌گونه که سید رضی تنظیم کرده حفظ شده است.</p>
<p>در حال حاضر هر ۴۸۰ حکمت، متن کامل نامه‌های ۱ تا ۲۰ و آغاز خطبه اول در دسترس است. بقیه متن‌ها به‌تدریج اضافه می‌شود. جستجو فقط متن‌های موجود را پوشش می‌دهد.</p>
<h2>حریم خصوصی</h2>
<p>هیچ حساب کاربری، ردیابی یا سرویس تحلیلی وجود ندارد. انتخاب زبان و حکمت‌های ذخیره‌شده فقط در مرورگر خودتان نگهداری می‌شود.</p>
</div>
<div class="en-only">
<p><strong>Nahj al-Balagha</strong> (“the path of eloquence”) is a selection of sermons, letters, and short sayings of Imam Ali ibn Abi Talib, compiled by <strong>al-Sharif al-Radi</strong> in the 4th century AH.</p>
<h2>Three main parts</h2>
<ul>
<li><strong>Sermons</strong> — about 241</li>
<li><strong>Letters</strong> — about 79</li>
<li><strong>Short sayings (Hikam)</strong> — about 480</li>
</ul>
<p>After the Quran, it is among the most important literary works in the Islamic world and has been translated into many languages.</p>
<h2>About this site</h2>
<p>imamali.xyz is a free static website with no accounts. The Arabic text is presented with Persian and English translations, and the book’s structure — sermons, letters, sayings — is kept exactly as al-Sharif al-Radi arranged it.</p>
<p>All 480 sayings, the full text of letters 1–20, and the opening of the first sermon are currently available. The remaining texts are being added gradually. Search covers the available texts only.</p>
<h2>Privacy</h2>
<p>There are no accounts, tracking, or analytics. Your language choice and saved sayings are kept only in your own browser.</p>
</div>
</article>
<aside class="about-aside">
<div class="fact-card"><h3>{bi('شروع خواندن', 'Start reading')}</h3><dl>
<dt>{bi('کوتاه و روزانه', 'Short and daily')}</dt><dd><a href="quote/1.html">{bi('کلمات قصار', 'Short sayings')}</a><small>{bi('۴۸۰ حکمت، ۲۰ حکمت در هر صفحه', '480 sayings, 20 per page')}</small></dd>
<dt>{bi('حکمت در عمل', 'Wisdom in practice')}</dt><dd><a href="rasail.html">{bi('نامه‌ها', 'Letters')}</a><small>{bi('از جمله عهدنامه مالک اشتر', 'Including the covenant to Malik al-Ashtar')}</small></dd>
<dt>{bi('خواندنی عمیق', 'Deeper reading')}</dt><dd><a href="khutbah.html">{bi('خطبه‌ها', 'Sermons')}</a><small>{bi('گزیده‌ای از خطبه‌ها', 'Selected sermons')}</small></dd>
</dl></div>
<div class="fact-card"><h3>{bi('میان‌برها', 'Shortcuts')}</h3><dl>
<dt>{bi('جستجو', 'Search')}</dt><dd><kbd>/</kbd> {bi('یا', 'or')} <kbd>Ctrl</kbd>+<kbd>K</kbd></dd>
<dt>{bi('صفحه قبل / بعد', 'Previous / next page')}</dt><dd>{bi('کلیدهای جهت‌نمای چپ و راست', 'Left and right arrow keys')}</dd>
<dt>{bi('زبان', 'Language')}</dt><dd>{bi('دکمه FA / EN در نوار بالا', 'FA / EN in the top bar')}</dd>
</dl></div>
<div class="fact-card"><h3>{bi('منبع باز', 'Open source')}</h3><p style="font-size:13px;line-height:1.9;color:#3d4654">{bi('فونت‌ها (Amiri، Vazirmatn، Cormorant Garamond) با مجوز SIL Open Font License هستند. تصویر صفحه اصلی تزئینی و تولیدشده با هوش مصنوعی است، نه عکس نسخه خطی واقعی.', 'The fonts (Amiri, Vazirmatn, Cormorant Garamond) are under the SIL Open Font License. The homepage image is decorative, AI-generated artwork, not a photograph of an authenticated manuscript.')}</p></div>
</aside>
</section>
</main>
{footer('')}'''
    write('about.html', head('', 'درباره نهج البلاغه | About Nahj al-Balagha',
                             'نهج البلاغه چیست؟ معرفی خطبه‌ها، نامه‌ها و کلمات قصار امام علی علیه‌السلام گردآوری سید رضی، و درباره سایت imamali.xyz.',
                             SITE + 'about.html') + body)


# ---------------------------------------------------------------- search
def build_search():
    topics = [('دانش', 'Knowledge'), ('عدالت', 'Justice'), ('صبر', 'Patience'), ('زندگی', 'Life'), ('دوستی', 'Friendship'), ('ایمان', 'Faith')]
    hints = ''.join(f'<a href="search.html?q={fa}" data-topic-fa="{fa}" data-topic-en="{en}">{bi(fa, en)}</a>' for fa, en in topics)
    body = f'''<body class="lang-fa site">
{topbar('', 'search')}
<main id="main">
{page_head('search', bi('جستجو', 'Search'), bi('جستجو در <em>گنجینه</em>', 'Search the <em>collection</em>'),
           bi('واژه، موضوع یا شماره را بنویسید. جستجو در همه ۴۸۰ حکمت، نامه‌های موجود و خطبه اول انجام می‌شود و در همین مرورگر اجرا می‌شود؛ چیزی ارسال نمی‌شود.',
              'Type a word, topic, or number. Search covers all 480 sayings, the available letters, and the first sermon, and runs entirely in your browser — nothing is sent anywhere.'),
           crumbs=[(bi('خانه', 'Home'), 'index.html'), (bi('جستجو', 'Search'), None)])}
<section class="home-wrap page-body">
<form class="search-page-form" id="searchForm" role="search">
<label class="visually-hidden" for="q">{bi('عبارت جستجو', 'Search query')}</label>
{icon('search')}<input type="search" id="q" name="q" placeholder="کلمه یا موضوع…" data-placeholder-fa="کلمه یا موضوع…" data-placeholder-en="Word or topic…" autocomplete="off" autofocus>
<button type="submit" class="gold-button">{bi('جستجو', 'Search')}</button>
</form>
<div class="search-hints"><span>{bi('پیشنهاد:', 'Try:')}</span>{hints}</div>
<div class="search-filters" role="group" aria-label="نوع متن" data-label-fa="نوع متن" data-label-en="Text type">
<button type="button" data-kind="all" aria-pressed="true">{bi('همه', 'All texts')}</button>
<button type="button" data-kind="wisdom" aria-pressed="false">{bi('حکمت‌ها', 'Wisdoms')}</button>
<button type="button" data-kind="letter" aria-pressed="false">{bi('نامه‌ها', 'Letters')}</button>
<button type="button" data-kind="sermon" aria-pressed="false">{bi('خطبه‌ها', 'Sermons')}</button>
</div>
<p id="status" class="list-status" role="status"></p>
<noscript><p class="empty-note">برای جستجو جاوااسکریپت را فعال کنید یا مستقیم <a href="quote/1.html">فهرست حکمت‌ها</a> را ببینید. · Enable JavaScript to search, or browse the <a href="quote/1.html">wisdoms</a> directly.</p></noscript>
<div id="results"></div>
<button type="button" class="gold-button" id="load-more" hidden>{bi('نتایج بیشتر', 'Load more results')}</button>
</section>
</main>
{footer('')}'''
    body = body.replace('<script src="site.js" defer></script>', '')
    write('search.html', head('', 'جستجو در نهج البلاغه | imamali.xyz', 'جستجو در خطبه‌ها، نامه‌ها و حکمت‌های نهج البلاغه — عربی، فارسی و انگلیسی.',
                              SITE + 'search.html', '<script src="search.js" defer></script>\n') + body)


# ---------------------------------------------------------------- 404 + hikam redirect
def build_misc():
    body = f'''<body class="lang-fa site">
{topbar('/', 'none')}
<main id="main"><section class="home-wrap notfound"><div>
<span class="brand-emblem" aria-hidden="true">ن</span>
<h1>{bi('این صفحه پیدا نشد', 'Page not found')}</h1>
<p>{bi('شاید نشانی تغییر کرده یا این متن هنوز اضافه نشده باشد.', 'The address may have changed, or this text has not been added yet.')}</p>
<div class="notfound-actions"><a class="gold-button" href="/index.html">{bi('صفحه اصلی', 'Go home')}</a><a class="gold-button" style="background:none;color:var(--navy);border-color:#d5d7d2" href="/search.html">{bi('جستجو', 'Search')}</a></div>
</div></section></main>
{footer('/')}'''
    write('404.html', head('/', 'صفحه پیدا نشد | نهج البلاغه', 'این صفحه در imamali.xyz وجود ندارد.', SITE + '404.html',
                           '<meta name="robots" content="noindex">\n') + body)


if __name__ == '__main__':
    build_khutbah()
    build_rasail()
    build_quotes()
    build_letters()
    build_excerpts()
    build_about()
    build_search()
    build_misc()
