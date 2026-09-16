(() => {
  'use strict';
  const input = document.getElementById('q');
  const results = document.getElementById('results');
  const status = document.getElementById('status');
  const more = document.getElementById('load-more');
  let kind = 'all', matches = [], shown = 0, version = 0, timer;
  const language = () => document.documentElement.lang === 'en' ? 'en' : 'fa';
  function showMore() {
    matches.slice(shown, shown + 20).forEach(item => results.append(window.NahjSearch.result(item, language())));
    shown = Math.min(shown + 20, matches.length);
    more.hidden = shown >= matches.length;
    status.textContent = language() === 'en' ? `${matches.length} results · ${shown} shown` : `${matches.length.toLocaleString('fa')} نتیجه · نمایش ${shown.toLocaleString('fa')} مورد`;
  }
  async function search(updateUrl = true) {
    const id = ++version;
    const query = input.value.trim();
    results.replaceChildren(); more.hidden = true; shown = 0;
    if (updateUrl) {
      const url = new URL(location.href);
      if (query) url.searchParams.set('q',query); else url.searchParams.delete('q');
      history.replaceState(null, '', url);
    }
    if (!query) {
      status.textContent = language() === 'en' ? 'Enter a word, topic, or text number to search the available library.' : 'برای جستجو در متن‌های موجود، واژه، موضوع یا شماره را وارد کنید.';
      return;
    }
    status.textContent = language() === 'en' ? 'Searching…' : 'در حال جستجو…';
    try {
      const found = await window.NahjSearch.find(query, kind);
      if (id !== version) return;
      matches = found;
      if (!matches.length) {
        status.textContent = language() === 'en' ? 'No matches. Try another word, a shorter phrase, or select All texts.' : 'نتیجه‌ای پیدا نشد. واژه‌ای دیگر، عبارتی کوتاه‌تر یا گزینه «همه» را امتحان کنید.';
        return;
      }
      showMore();
    } catch {
      if (id === version) status.textContent = language() === 'en' ? 'Search could not load. Check your connection, then press Search to retry.' : 'جستجو بارگذاری نشد. اتصال را بررسی کنید و برای تلاش دوباره دکمه جستجو را بزنید.';
    }
  }
  const params = new URLSearchParams(location.search);
  input.value = params.get('q') || '';
  if (['wisdom','letter','sermon'].includes(params.get('kind'))) {
    kind = params.get('kind');
    document.querySelectorAll('[data-kind]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.kind === kind)));
  }
  const updateTopics = () => document.querySelectorAll('[data-topic-fa]').forEach(a => a.href = 'search.html?q=' + encodeURIComponent(a.dataset[language() === 'en' ? 'topicEn' : 'topicFa']));
  updateTopics();
  document.getElementById('searchForm').addEventListener('submit', e => { e.preventDefault(); clearTimeout(timer); search(); });
  input.addEventListener('input', () => { ++version; clearTimeout(timer); timer = setTimeout(search,180); });
  document.querySelectorAll('[data-kind]').forEach(button => button.addEventListener('click', () => {
    kind = button.dataset.kind;
    document.querySelectorAll('[data-kind]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    search();
  }));
  more.addEventListener('click', () => {
    const previousCount = results.children.length;
    showMore();
    results.children[previousCount]?.focus({preventScroll:true});
  });
  new MutationObserver(() => { updateTopics(); search(false); }).observe(document.documentElement, {attributes:true,attributeFilter:['lang']});
  search(false);
})();
