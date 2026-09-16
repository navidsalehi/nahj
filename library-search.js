/* Static, on-demand search. No service, tracking, or runtime dependencies. */
(() => {
  'use strict';
  let indexPromise;
  const base = () => (document.body && document.body.dataset.root) || '';
  const normalize = value => String(value).toLowerCase().normalize('NFKD')
    .replace(/[\u064B-\u065F\u0670\u0640\u200c\u200d]/g, '')
    .replace(/[يى]/g, 'ی').replace(/ك/g, 'ک').replace(/[أإآ]/g, 'ا')
    .replace(/[۰-۹]/g, digit => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(digit)))
    .replace(/[٠-٩]/g, digit => String('٠١٢٣٤٥٦٧٨٩'.indexOf(digit)));
  async function load() {
    if (!indexPromise) {
      indexPromise = fetch(base() + 'assets/search-index.json').then(response => {
        if (!response.ok) throw new Error('Index unavailable');
        return response.json();
      }).then(items => items.map(item => ({ ...item,
        haystack: normalize([item.fa, item.en, item.ar, item.bodyFa, item.bodyEn].join(' '))
      }))).catch(error => { indexPromise = null; throw error; });
    }
    return indexPromise;
  }
  async function find(query, kind = 'all') {
    const words = normalize(query.trim()).split(/\s+/).filter(Boolean);
    if (!words.length) return [];
    return (await load()).filter(item => (kind === 'all' || item.kind === kind) &&
      words.every(word => item.haystack.includes(word)));
  }
  function result(item, lang, root = base()) {
    const en = lang === 'en';
    const a = document.createElement('a');
    a.className = 'search-result';
    a.href = root + item.url;
    const small = document.createElement('small');
    small.textContent = ({wisdom:en?'Wisdom':'حکمت',letter:en?'Letter':'نامه',sermon:en?'Sermon':'خطبه'})[item.kind];
    const title = document.createElement('strong');
    title.textContent = (en ? item.en : item.fa) || item.fa;
    const excerpt = document.createElement('p');
    const body = (en ? item.bodyEn : item.bodyFa) || item.ar;
    excerpt.textContent = body.length > 180 ? body.slice(0,180) + '…' : body;
    if (en && !item.bodyEn) { excerpt.dir = 'rtl'; excerpt.lang = 'ar'; }
    a.append(small, title, excerpt);
    return a;
  }
  window.NahjSearch = { find, result };
})();
