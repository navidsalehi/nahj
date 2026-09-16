(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const storage = {
    get(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } },
    set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); return true; } catch { return false; } }
  };
  let lang = 'fa';
  let wisdomIndex = 0;
  const wisdoms = JSON.parse($('#initial-wisdoms').textContent);
  const stored = storage.get('nahj-saved', []);
  let saved = Array.isArray(stored) ? stored.filter(n => Number.isInteger(n)) : [];
  let toastTimer;
  function toast(fa, en) {
    $('#toast').textContent = lang === 'en' ? en : fa;
    $('#toast').classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => $('#toast').classList.remove('show'), 3500);
  }
  function renderWisdom() {
    const item = wisdoms[wisdomIndex];
    $('#wisdom-content blockquote').textContent = item.ar;
    $('.wisdom-translation .fa-only').textContent = item.bodyFa;
    $('.wisdom-translation .en-only').textContent = item.bodyEn;
    $('#wisdom-source').href = item.url;
    $('#wisdom-source').textContent = lang === 'en' ? item.en : 'حکمت ' + item.number.toLocaleString('fa');
    const isSaved = saved.includes(item.number);
    $('#save-wisdom').setAttribute('aria-pressed', String(isSaved));
    $('#save-wisdom').setAttribute('aria-label', lang === 'en' ? (isSaved ? 'Unsave wisdom' : 'Save wisdom') : (isSaved ? 'حذف از ذخیره‌ها' : 'ذخیره حکمت'));
    $$('.quote-dots i').forEach((dot, i) => dot.classList.toggle('selected', i === wisdomIndex));
  }
  function renderSaved() {
    const items = wisdoms.filter(item => saved.includes(item.number));
    $('#saved-section').hidden = !items.length;
    $('#saved-list').replaceChildren();
    items.forEach(item => {
      const card = document.createElement('article'); card.className = 'saved-item';
      const a = document.createElement('a'); a.href = item.url;
      a.textContent = lang === 'en' ? item.en : 'حکمت ' + item.number.toLocaleString('fa');
      const p = document.createElement('p'); p.textContent = item.ar; p.lang = 'ar'; p.dir = 'rtl';
      a.append(p);
      const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'icon-button'; remove.textContent = '×';
      remove.setAttribute('aria-label', lang === 'en' ? `Remove wisdom ${item.number}` : `حذف حکمت ${item.number}`);
      remove.addEventListener('click', () => {
        const next = saved.filter(n => n !== item.number);
        if (!storage.set('nahj-saved', next)) { toast('ذخیره‌سازی مرورگر در دسترس نیست.','Browser storage is unavailable.'); return; }
        saved = next; renderSaved(); renderWisdom();
        const focusTarget = $('#saved-list button') || $('#save-wisdom');
        focusTarget.focus({preventScroll:true});
        toast('حکمت از ذخیره‌ها حذف شد.','Wisdom removed from saved.');
      });
      card.append(a, remove); $('#saved-list').append(card);
    });
  }
  function applyLang(value) {
    lang = value === 'en' ? 'en' : 'fa';
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'en' ? 'ltr' : 'rtl';
    document.body.classList.toggle('lang-fa', lang === 'fa');
    document.body.classList.toggle('lang-en', lang === 'en');
    $$('.lang-switch button').forEach(button => {
      const active = button.dataset.lang === lang;
      button.classList.toggle('on', active); button.setAttribute('aria-pressed', String(active));
    });
    $$('[data-label-fa]').forEach(el => el.setAttribute('aria-label', el.dataset[lang === 'en' ? 'labelEn' : 'labelFa']));
    $$('[data-topic-fa]').forEach(el => el.href = 'search.html?q=' + encodeURIComponent(el.dataset[lang === 'en' ? 'topicEn' : 'topicFa']));
    $('#quick-query').placeholder = lang === 'en' ? 'Search a word or topic…' : 'کلمه یا موضوعی بنویسید…';
    try { localStorage.setItem('nahj-lang', lang); } catch { /* Reading works without storage. */ }
    renderWisdom(); renderSaved();
    if ($('#search-dialog').open) runSearch();
  }
  let initialLang = 'fa';
  try { initialLang = localStorage.getItem('nahj-lang') || 'fa'; } catch { /* Use default. */ }
  applyLang(initialLang);
  $$('.lang-switch button').forEach(button => button.addEventListener('click', () => applyLang(button.dataset.lang)));

  const menu = $('#menu-btn');
  function setMenu(open, restore = false) {
    $('#primary-nav').classList.toggle('open', open);
    menu.classList.toggle('is-open', open); menu.setAttribute('aria-expanded', String(open));
    if (restore) menu.focus();
  }
  menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
  $$('#primary-nav a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  document.addEventListener('click', e => { if (!e.target.closest('.topbar')) setMenu(false); });
  document.addEventListener('focusin', e => { if (!e.target.closest('.topbar')) setMenu(false); });
  matchMedia('(min-width:801px)').addEventListener('change', () => setMenu(false));

  $('#next-wisdom').addEventListener('click', () => { wisdomIndex = (wisdomIndex + 1) % wisdoms.length; renderWisdom(); });
  $('#save-wisdom').addEventListener('click', () => {
    const id = wisdoms[wisdomIndex].number;
    const removing = saved.includes(id);
    const next = removing ? saved.filter(n => n !== id) : [...saved, id];
    if (!storage.set('nahj-saved', next)) { toast('ذخیره‌سازی مرورگر در دسترس نیست.','Browser storage is unavailable.'); return; }
    saved = next; renderWisdom(); renderSaved();
    toast(removing ? 'حکمت از ذخیره‌ها حذف شد.' : 'در همین مرورگر ذخیره شد.', removing ? 'Wisdom removed from saved.' : 'Wisdom saved in this browser.');
  });
  $('#share-wisdom').addEventListener('click', async () => {
    const item = wisdoms[wisdomIndex];
    const url = new URL(item.url, location.href).href;
    const text = item.ar + '\n\n' + (lang === 'en' ? item.bodyEn : item.bodyFa);
    try {
      if (navigator.share) await navigator.share({title:'Nahj al-Balagha', text, url});
      else if (navigator.clipboard) { await navigator.clipboard.writeText(text + '\n' + url); toast('متن و پیوند کپی شد.','Wisdom and link copied.'); }
      else toast('برای اشتراک، پیوند حکمت را باز کرده و کپی کنید.','Open the wisdom link and copy its address to share.');
    } catch (error) { if (error.name !== 'AbortError') toast('اشتراک ممکن نشد؛ پیوند حکمت را کپی کنید.','Could not share. Open the wisdom link and copy its address.'); }
  });

  const dialog = $('#search-dialog');
  let previousFocus;
  function openSearch() {
    if (dialog.open) return;
    previousFocus = document.activeElement;
    setMenu(false); dialog.showModal(); document.body.style.overflow = 'hidden';
    $('#quick-query').focus(); runSearch();
  }
  $('#open-search').addEventListener('click', openSearch);
  $('#close-search').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { document.body.style.overflow = ''; previousFocus?.focus(); });
  dialog.addEventListener('click', e => {
    const rect = dialog.getBoundingClientRect();
    if (e.target === dialog && (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom)) dialog.close();
  });
  document.addEventListener('keydown', e => {
    const typing = e.target.matches('input,textarea,[contenteditable]');
    if ((e.key.toLowerCase() === 'k' && (e.ctrlKey || e.metaKey)) || (e.key === '/' && !typing)) { e.preventDefault(); openSearch(); }
    if (e.key === 'Escape' && dialog.open) { e.preventDefault(); dialog.close(); }
    else if (e.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') setMenu(false, true);
  });
  let searchTimer, searchVersion = 0;
  async function runSearch() {
    const version = ++searchVersion;
    const query = $('#quick-query').value.trim();
    const status = $('#quick-status');
    $('#quick-results').replaceChildren();
    if (!query) { status.textContent = lang === 'en' ? 'Search the available sermons, letters, and wisdoms.' : 'در خطبه‌ها، نامه‌ها و حکمت‌های موجود جستجو کنید.'; return; }
    status.textContent = lang === 'en' ? 'Searching…' : 'در حال جستجو…';
    try {
      const items = await window.NahjSearch.find(query);
      if (version !== searchVersion) return;
      status.textContent = items.length ? (lang === 'en' ? `${items.length} results · showing the first ${Math.min(5,items.length)}` : `${items.length.toLocaleString('fa')} نتیجه · نمایش ${Math.min(5,items.length).toLocaleString('fa')} مورد اول`) : (lang === 'en' ? 'No matches. Try a different word or a shorter phrase.' : 'نتیجه‌ای پیدا نشد. واژه‌ای دیگر یا عبارتی کوتاه‌تر بنویسید.');
      items.slice(0,5).forEach(item => $('#quick-results').append(window.NahjSearch.result(item, lang)));
      if (items.length > 5) {
        const all = document.createElement('a'); all.className = 'text-link'; all.href = 'search.html?q=' + encodeURIComponent(query);
        all.textContent = lang === 'en' ? 'View all results →' : 'مشاهده همه نتایج ←'; $('#quick-results').append(all);
      }
    } catch {
      if (version === searchVersion) status.textContent = lang === 'en' ? 'Search could not load. Check your connection and try again.' : 'جستجو بارگذاری نشد. اتصال را بررسی و دوباره تلاش کنید.';
    }
  }
  $('#quick-query').addEventListener('input', () => { ++searchVersion; clearTimeout(searchTimer); searchTimer = setTimeout(runSearch, 180); });

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  if ('IntersectionObserver' in window && !reduced.matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('in-view'); observer.unobserve(entry.target); }
    }), {threshold:.08, rootMargin:'0px 0px -25px 0px'});
    document.body.classList.add('motion-ready');
    $$('.motion-reveal').forEach(el => observer.observe(el));
    // Keyboard navigation must never land in an invisible section.
    document.addEventListener('focusin', e => e.target.closest('.motion-reveal')?.classList.add('in-view'));
  }
  let framePending = false;
  function updateProgress() {
    const max = document.documentElement.scrollHeight - innerHeight;
    $('.reading-progress').style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`;
    framePending = false;
  }
  addEventListener('scroll', () => { if (!framePending) { framePending = true; requestAnimationFrame(updateProgress); } }, {passive:true});
  addEventListener('resize', updateProgress); updateProgress();
})();
