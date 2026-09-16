/* Inner-page smoke suite. Run against npm run dev (see README). */
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;
const base = process.env.TEST_URL || 'http://127.0.0.1:3000';
const pages = ['/khutbah.html','/rasail.html','/quote/1.html','/quote/24.html','/letter/1.html','/letter/20.html','/about.html','/search.html?q=knowledge','/khutbah-detail.html','/rasail-detail.html','/404.html'];
(async () => {
  const options = { headless:true };
  if (process.env.CHROMIUM_EXECUTABLE_PATH) options.executablePath = process.env.CHROMIUM_EXECUTABLE_PATH;
  const browser = await chromium.launch(options);
  try {
    for (const path of pages) for (const lang of ['fa','en']) {
      const context = await browser.newContext({ viewport:{width:1440,height:1000}, reducedMotion:'reduce' });
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.addInitScript(l => { try { localStorage.setItem('nahj-lang', l); } catch {} }, lang);
      await page.goto(base + path, { waitUntil:'networkidle' });
      assert.equal(await page.getAttribute('html','dir'), lang === 'en' ? 'ltr' : 'rtl', `${path} ${lang} direction`);
      for (const width of [320,390,768,1024,1440]) {
        await page.setViewportSize({width,height:900});
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `${path} ${lang} overflow at ${width}`);
      }
      await page.setViewportSize({width:1440,height:1000});
      const audit = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
      assert.deepEqual(audit.violations.map(v => ({id:v.id,targets:v.nodes.map(n => n.target)})), [], `${path} ${lang} accessibility`);
      assert.deepEqual(errors, [], `${path} ${lang} runtime errors`);
      await context.close();
    }
    const context = await browser.newContext({ viewport:{width:1280,height:900} });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(base + '/quote/1.html');
    await page.fill('#filter','فتنه');
    assert.equal(await page.locator('.hikam-card:visible').count(), 1);
    await page.fill('#filter','zzz');
    assert.equal(await page.locator('#list-empty').isVisible(), true);
    await page.fill('#filter','');
    assert.equal(await page.locator('.hikam-card .card-actions button').count(), 40);
    await page.keyboard.press('Control+k');
    assert.equal(await page.locator('#search-dialog').evaluate(d => d.open), true);
    await page.fill('#quick-query','علم');
    await page.waitForSelector('#quick-results .search-result');
    assert.match(await page.locator('#quick-results .search-result').first().getAttribute('href'), /^\.\.\//, 'search results resolve from a subfolder');
    await page.keyboard.press('Escape');
    await page.fill('#jump','۴۵');
    await page.click('#jump-form button');
    await page.waitForURL(/quote\/3\.html#wisdom-45/);
    await page.keyboard.press('ArrowLeft');
    await page.waitForURL(/quote\/4\.html/);
    await page.evaluate(() => {
      Object.defineProperty(navigator,'share',{value:undefined,configurable:true});
      Object.defineProperty(navigator,'clipboard',{value:{writeText:async text => window.sharedText = text},configurable:true});
    });
    await page.locator('.hikam-card .btn-share').first().click();
    assert.match(await page.evaluate(() => window.sharedText), /#wisdom-61/);
    await page.goto(base + '/rasail.html');
    assert.equal(await page.locator('#list .entry').count(), 79);
    await page.click('[data-show="available"]');
    assert.equal(await page.locator('#list .entry:visible').count(), 20);
    await page.click('[data-show="all"]');
    await page.fill('#filter','معاویه');
    assert(await page.locator('#list .entry:visible').count() > 5);
    await page.goto(base + '/letter/5.html');
    await page.keyboard.press('ArrowLeft');
    await page.waitForURL(/letter\/6\.html/);
    await page.locator('[data-lang="en"]').click();
    await page.keyboard.press('ArrowLeft');
    await page.waitForURL(/letter\/5\.html/);
    await page.goto(base + '/khutbah.html');
    await page.fill('#filter','193');
    assert.equal(await page.locator('#list .entry:visible').count(), 1);
    await page.goto(base + '/search.html?q=god&kind=letter');
    await page.waitForSelector('#results .search-result');
    assert.equal(await page.locator('[data-kind="letter"]').getAttribute('aria-pressed'), 'true');
    assert((await page.locator('#results small').allTextContents()).every(t => t === 'Letter'));
    assert.deepEqual(errors, [], 'No JS runtime errors');
    await context.close();
    console.log('PASS: inner pages — FA/EN, 5 viewport sizes, accessibility, filters, jump, dialog search from subfolders, keyboard paging, share fallback, letter chips, search kind filter.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
