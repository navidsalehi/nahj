/* Shared behaviour for every inner page: language, menu, search dialog, toast,
   reading progress, list filters, wisdom/letter audio and share. No dependencies. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  const root = document.documentElement;
  const base = document.body.dataset.root || '';
  let lang = 'fa';
  const en = () => lang === 'en';
  const faNum = n => Number(n).toLocaleString('fa');
  const t = (fa, enText) => (en() ? enText : fa);

  /* Toast */
  let toastTimer;
  function toast(fa, enText) {
    const el = $('#toast'); if (!el) return;
    el.textContent = t(fa, enText); el.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('show'), 3500);
  }

  /* Language */
  function applyLang(value) {
    lang = value === 'en' ? 'en' : 'fa';
    root.lang = lang; root.dir = en() ? 'ltr' : 'rtl';
    document.body.classList.toggle('lang-fa', !en());
    document.body.classList.toggle('lang-en', en());
    $$('.lang-switch [data-lang]').forEach(b => {
      const on = b.dataset.lang === lang;
      b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on));
    });
    $$('[data-label-fa]').forEach(el => el.setAttribute('aria-label', en() ? el.dataset.labelEn : el.dataset.labelFa));
    $$('[data-placeholder-fa]').forEach(el => el.placeholder = en() ? el.dataset.placeholderEn : el.dataset.placeholderFa);
    $$('[data-title-fa]').forEach(el => el.title = en() ? el.dataset.titleEn : el.dataset.titleFa);
    try { localStorage.setItem('nahj-lang', lang); } catch { /* reading works without storage */ }
    document.dispatchEvent(new CustomEvent('nahj:lang', { detail: lang }));
  }
  let initial = 'fa';
  try { initial = localStorage.getItem('nahj-lang') || 'fa'; } catch { /* default */ }
  applyLang(initial);
  $$('.lang-switch [data-lang]').forEach(b => b.addEventListener('click', () => applyLang(b.dataset.lang)));

  /* Menu */
  const menu = $('#menu-btn'), nav = $('#primary-nav');
  function setMenu(open, restore = false) {
    if (!menu || !nav) return;
    nav.classList.toggle('open', open);
    menu.classList.toggle('is-open', open); menu.setAttribute('aria-expanded', String(open));
    if (restore) menu.focus();
  }
  if (menu && nav) {
    menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
    $$('#primary-nav a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    document.addEventListener('click', e => { if (!e.target.closest('.topbar')) setMenu(false); });
    document.addEventListener('focusin', e => { if (!e.target.closest('.topbar')) setMenu(false); });
    matchMedia('(min-width:801px)').addEventListener('change', () => setMenu(false));
  }

  /* Reading progress */
  const progress = $('.reading-progress');
  if (progress) {
    const update = () => {
      const max = root.scrollHeight - innerHeight;
      progress.style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`;
    };
    addEventListener('scroll', update, { passive: true }); addEventListener('resize', update); update();
  }

  /* Search dialog */
  const dialog = $('#search-dialog');
  if (dialog && window.NahjSearch) {
    const input = $('#quick-query'), status = $('#quick-status'), results = $('#quick-results');
    let previousFocus, timer, version = 0;
    function openSearch() {
      if (dialog.open) return;
      previousFocus = document.activeElement;
      setMenu(false); dialog.showModal(); document.body.style.overflow = 'hidden';
      input.focus(); run();
    }
    async function run() {
      const id = ++version, query = input.value.trim();
      results.replaceChildren();
      if (!query) { status.textContent = t('در خطبه‌ها، نامه‌ها و حکمت‌های موجود جستجو کنید.', 'Search the available sermons, letters, and wisdoms.'); return; }
      status.textContent = t('در حال جستجو…', 'Searching…');
      try {
        const items = await window.NahjSearch.find(query);
        if (id !== version) return;
        status.textContent = items.length
          ? t(`${faNum(items.length)} نتیجه · نمایش ${faNum(Math.min(5, items.length))} مورد اول`, `${items.length} results · showing the first ${Math.min(5, items.length)}`)
          : t('نتیجه‌ای پیدا نشد. واژه‌ای دیگر یا عبارتی کوتاه‌تر بنویسید.', 'No matches. Try a different word or a shorter phrase.');
        items.slice(0, 5).forEach(item => results.append(window.NahjSearch.result(item, lang, base)));
        if (items.length > 5) {
          const all = document.createElement('a'); all.className = 'text-link'; all.href = base + 'search.html?q=' + encodeURIComponent(query);
          all.textContent = t('مشاهده همه نتایج ←', 'View all results →'); results.append(all);
        }
      } catch {
        if (id === version) status.textContent = t('جستجو بارگذاری نشد. اتصال را بررسی و دوباره تلاش کنید.', 'Search could not load. Check your connection and try again.');
      }
    }
    $('#open-search')?.addEventListener('click', openSearch);
    $('#close-search')?.addEventListener('click', () => dialog.close());
    dialog.addEventListener('close', () => { document.body.style.overflow = ''; previousFocus?.focus(); });
    dialog.addEventListener('click', e => {
      const r = dialog.getBoundingClientRect();
      if (e.target === dialog && (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom)) dialog.close();
    });
    input.addEventListener('input', () => { ++version; clearTimeout(timer); timer = setTimeout(run, 180); });
    document.addEventListener('nahj:lang', () => { if (dialog.open) run(); });
    document.addEventListener('keydown', e => {
      const typing = e.target.matches('input,textarea,[contenteditable]');
      if ((e.key.toLowerCase() === 'k' && (e.ctrlKey || e.metaKey)) || (e.key === '/' && !typing)) { e.preventDefault(); openSearch(); }
      if (e.key === 'Escape' && dialog.open) { e.preventDefault(); dialog.close(); }
      else if (e.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') setMenu(false, true);
    });
  }

  /* In-page list filter (sermons, letters, wisdoms) */
  const filter = $('#filter'), list = $('#list');
  if (filter && list) {
    const items = $$('#list [data-s], #list .entry, #list .hikam-card');
    const status = $('#list-status'), empty = $('#list-empty');
    const norm = v => String(v).toLowerCase().normalize('NFKD')
      .replace(/[\u064B-\u065F\u0670\u0640\u200c\u200d]/g, '').replace(/[يى]/g, 'ی').replace(/ك/g, 'ک').replace(/[أإآ]/g, 'ا')
      .replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d)).replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d));
    const hay = new Map(items.map(el => [el, norm((el.dataset.s || '') + ' ' + el.textContent)]));
    function apply() {
      const words = norm(filter.value.trim()).split(/\s+/).filter(Boolean);
      let shown = 0;
      items.forEach(el => { const ok = words.every(w => hay.get(el).includes(w)); el.hidden = !ok; if (ok) shown++; });
      if (empty) empty.hidden = shown > 0;
      if (status) status.textContent = words.length
        ? t(`${faNum(shown)} از ${faNum(items.length)} مورد`, `${shown} of ${items.length} shown`)
        : (status.dataset[en() ? 'defaultEn' : 'defaultFa'] || '');
    }
    filter.addEventListener('input', apply);
    document.addEventListener('nahj:lang', apply);
    const params = new URLSearchParams(location.search);
    if (params.get('q')) filter.value = params.get('q');
    apply();
  }

  /* Jump to a wisdom by number */
  const jump = $('#jump-form');
  if (jump) jump.addEventListener('submit', e => {
    e.preventDefault();
    const raw = jump.querySelector('input').value.trim().replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d)).replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d));
    const n = parseInt(raw, 10);
    if (!n || n < 1 || n > 480) { toast('شماره‌ای بین ۱ تا ۴۸۰ وارد کنید.', 'Enter a number between 1 and 480.'); return; }
    location.href = `${Math.ceil(n / 20)}.html#wisdom-${n}`;
  });

  /* Audio + share for wisdom cards and letters */
  const synth = window.speechSynthesis;
  let activeButton;
  function speak(text, button) {
    if (!synth) { toast('مرورگر شما خواندن صوتی را پشتیبانی نمی‌کند.', 'Your browser does not support speech playback.'); return; }
    if (synth.speaking) {
      synth.cancel(); activeButton?.classList.remove('playing');
      if (activeButton === button) { activeButton = null; return; }
    }
    const u = new SpeechSynthesisUtterance(text); u.lang = 'ar-SA'; u.rate = 0.88;
    const voice = synth.getVoices().find(v => v.lang && v.lang.startsWith('ar'));
    if (voice) u.voice = voice;
    else toast('صدای عربی در این دستگاه نصب نیست؛ تلفظ ممکن است دقیق نباشد.', 'No Arabic voice is installed on this device; pronunciation may be inexact.');
    const stop = () => { button.classList.remove('playing'); if (activeButton === button) activeButton = null; };
    u.onend = stop; u.onerror = stop;
    button.classList.add('playing'); activeButton = button; synth.speak(u);
  }
  async function share(title, text, url) {
    try {
      if (navigator.share) await navigator.share({ title, text, url });
      else if (navigator.clipboard) { await navigator.clipboard.writeText(text + '\n' + url); toast('متن و پیوند کپی شد.', 'Text and link copied.'); }
      else toast('برای اشتراک، نشانی صفحه را کپی کنید.', 'Copy the page address to share.');
    } catch (err) { if (err.name !== 'AbortError') toast('اشتراک ممکن نشد؛ نشانی صفحه را کپی کنید.', 'Could not share. Copy the page address instead.'); }
  }
  if (synth) { synth.getVoices(); synth.onvoiceschanged = () => synth.getVoices(); }
  const icon = d => `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${d}"/></svg>`;
  const ICON_AUDIO = 'M4 10v4h4l5 4V6l-5 4H4Zm12-1a4 4 0 0 1 0 6m2.5-9a8 8 0 0 1 0 12';
  const ICON_SHARE = 'M12 15V3m-4 4 4-4 4 4M5 12v8h14v-8';
  $$('.hikam-card').forEach(card => {
    if (card.querySelector('.card-actions')) return;
    const ar = card.querySelector('.ar'), fa = card.querySelector('.tr.fa-only'), enT = card.querySelector('.tr.en-only'), num = card.querySelector('.num');
    const actions = document.createElement('div'); actions.className = 'card-actions';
    actions.innerHTML =
      `<button type="button" class="btn-audio">${icon(ICON_AUDIO)}<span class="fa-only">شنیدن</span><span class="en-only">Listen</span></button>` +
      `<button type="button" class="btn-share">${icon(ICON_SHARE)}<span class="fa-only">اشتراک</span><span class="en-only">Share</span></button>`;
    card.append(actions);
    actions.querySelector('.btn-audio').addEventListener('click', function () { if (ar) speak(ar.textContent, this); });
    actions.querySelector('.btn-share').addEventListener('click', () => {
      const url = location.origin + location.pathname + '#' + card.id;
      const title = num ? num.textContent : 'Nahj al-Balagha';
      const text = (ar ? ar.textContent + '\n\n' : '') + ((en() && enT ? enT : fa)?.textContent || '') + '\n\n' + title;
      share(title, text, url);
    });
  });
  const arText = $('#arText');
  if (arText) {
    $('#btnAudio')?.addEventListener('click', function () { speak(arText.textContent, this); });
    $('#btnShare')?.addEventListener('click', () => {
      const body = en() ? $('.letter-block.en-only .tr-body') : $('.letter-block.fa-only .tr-body');
      share(document.title, arText.textContent + '\n\n' + (body?.textContent || ''), location.href);
    });
    $('#btnCopy')?.addEventListener('click', async () => {
      const body = en() ? $('.letter-block.en-only .tr-body') : $('.letter-block.fa-only .tr-body');
      try { await navigator.clipboard.writeText(arText.textContent + '\n\n' + (body?.textContent || '')); toast('متن کپی شد.', 'Text copied.'); }
      catch { toast('کپی ممکن نشد.', 'Could not copy.'); }
    });
    $('#btnPrint')?.addEventListener('click', () => print());
  }

  /* Keyboard: ← → between letters / wisdom pages */
  const prev = $('[data-nav="prev"]'), next = $('[data-nav="next"]');
  if (prev || next) document.addEventListener('keydown', e => {
    if (e.altKey || e.ctrlKey || e.metaKey || e.target.matches('input,textarea')) return;
    const forward = en() ? 'ArrowRight' : 'ArrowLeft', back = en() ? 'ArrowLeft' : 'ArrowRight';
    if (e.key === forward && next?.href) location.href = next.href;
    if (e.key === back && prev?.href) location.href = prev.href;
  });

  /* Reveal */
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  if ('IntersectionObserver' in window && !reduced.matches && $('.motion-reveal')) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('in-view'); observer.unobserve(entry.target); }
    }), { threshold: .08, rootMargin: '0px 0px -25px 0px' });
    document.body.classList.add('motion-ready');
    $$('.motion-reveal').forEach(el => observer.observe(el));
  }
})();
