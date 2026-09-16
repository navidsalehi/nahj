# نهج البلاغه | Imam Ali

سایت استاتیک نهج البلاغه — خطبه‌ها، نامه‌ها و ۴۸۰ کلمه قصار با ترجمه فارسی و انگلیسی.

**دامنه:** [https://imamali.xyz](https://imamali.xyz)

## ساختار

- `index.html` — صفحه اصلی
- `khutbah.html` / `rasail.html` — خطبه‌ها و نامه‌ها
- `quote/1.html` … `quote/24.html` — کلمات قصار (هر صفحه ۲۰ حکمت)
- `letter/1.html` … `letter/20.html` — متن کامل نامه‌ها (بقیه به‌تدریج)
- `search.html` — جستجو · `404.html` — صفحه پیدا نشد
- `about.html` — درباره
- `sitemap.xml` / `robots.txt` — سئو
- `CNAME` — دامنه سفارشی GitHub Pages

## انتشار با GitHub Pages

1. این پوشه را به یک مخزن GitHub پوش کنید.
2. Settings → Pages → Source: Deploy from branch `main` / root
3. دامنه `imamali.xyz` را در Settings → Pages → Custom domain وارد کنید.
4. در DNS دامنه، رکوردهای لازم را تنظیم کنید (راهنما داخل مخزن / پیام راهنما).

## زبان

تغییر زبان FA / EN از نوار بالا؛ انتخاب در `localStorage` ذخیره می‌شود.

## Modern homepage & local development

The homepage is still plain static HTML/CSS/JavaScript—no build step or backend is required for GitHub Pages.

```sh
python3 -m http.server 3000 --bind 0.0.0.0
```

- `site.css` / `site.js`: shared chrome for every inner page (topbar, footer, search dialog, toast, reading progress, list filters, wisdom/letter audio + share, keyboard paging with ← →). Inner pages load `style.css` + `site.css`; the homepage additionally loads `home.css`.
- `scripts/build-pages.py`: regenerates `khutbah.html`, `rasail.html`, `quote/*.html`, `letter/*.html`, the two detail excerpts, `about.html`, `search.html`, and `404.html` from the existing texts (wisdom cards and letter bodies are copied verbatim; the letter index comes from `assets/letters.json`). Standard library only — run `python3 scripts/build-pages.py` after editing a text, then rebuild the search index below.
- `home.css` / `home.js`: responsive editorial homepage, progressive scroll reveals, reading progress, accessible search dialog (`/` or Ctrl/Cmd+K), and featured wisdom save/share controls.
- `library-search.js` / `search.js`: on-demand, client-side Arabic/Persian/English search and category filtering. Search covers **existing content only**, not missing editions or unavailable translations.
- `assets/search-index.json`: generated index of the 480 wisdoms, 20 available letter pages, and the existing first sermon detail.
- `assets/featured.json`: five texts copied directly from the existing wisdom pages. The homepage embeds this small set for instant, offline-friendly rendering.
- Saved featured wisdoms stay in this browser (`nahj-saved`); there is no account, synchronization, or tracking. Language continues to use `nahj-lang`.
- Fonts are self-hosted, with their SIL Open Font Licenses in `assets/fonts`. The WebP hero is AI-generated decorative imagery, not a photograph of an authenticated manuscript.

### Updating the search index

After editing the source texts:

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/build-search.py
```

The script also adds stable `#wisdom-N` anchors without rewriting or modifying the text. If a featured text changes, update the `initial-wisdoms` JSON and initial quotation in `index.html` to match `assets/featured.json`.

### Browser checks

With the local server running:

```sh
npm install
npx playwright install --with-deps chromium
npm test
```

`tests/homepage.cjs` covers Persian/English, horizontal overflow at 320/390/768/1024/1440px, menu and search keyboard behavior, search filters and empty states, saved wisdom persistence/removal, featured text rotation, the share fallback, deep links, and no-JavaScript content visibility. Axe checks the homepage, search dialog, and search page against WCAG A/AA rules; this is automated coverage, not a complete accessibility certification.

`tests/pages.cjs` runs the same language, overflow, and axe checks on every inner page type (lists, wisdom pages, letter reader, detail excerpts, about, search, 404) plus the in-page filter, wisdom jump box, dialog search from subfolders, arrow-key paging, share fallback, the letters "full text only" chip, and the search `kind` parameter.

Optional test settings: `TEST_URL` for another server and `CHROMIUM_EXECUTABLE_PATH` for an existing Chromium installation.
