/* Run against npm run dev; browser defaults to Playwright's installed Chromium. */
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;
const base = process.env.TEST_URL || 'http://127.0.0.1:3000';
(async () => {
  const options = { headless:true };
  if (process.env.CHROMIUM_EXECUTABLE_PATH) options.executablePath = process.env.CHROMIUM_EXECUTABLE_PATH;
  const browser = await chromium.launch(options);
  try {
    const context = await browser.newContext({ viewport:{width:1440,height:1000}, reducedMotion:'reduce' });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(base);
    assert.equal(await page.getAttribute('html','dir'),'rtl');
    await page.locator('[data-lang="en"]').click();
    assert.equal(await page.getAttribute('html','dir'),'ltr');
    await page.reload();
    assert.equal(await page.getAttribute('html','lang'),'en');
    for (const lang of ['en','fa']) {
      await page.locator(`[data-lang="${lang}"]`).click();
      for (const width of [320,390,768,1024,1440]) {
        await page.setViewportSize({width,height:900});
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth),false,`${lang} overflow at ${width}`);
      }
      const audit = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
      assert.deepEqual(audit.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})),[],`${lang} accessibility`);
    }
    await page.locator('[data-lang="en"]').click();
    await page.setViewportSize({width:390,height:844});
    await page.locator('#menu-btn').click();
    assert.equal(await page.locator('#menu-btn').getAttribute('aria-expanded'),'true');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#menu-btn').getAttribute('aria-expanded'),'false');
    await page.keyboard.press('Control+k');
    assert.equal(await page.locator('#search-dialog').evaluate(el=>el.open),true);
    await page.locator('#quick-query').fill('knowledge');
    await page.waitForFunction(()=>document.querySelectorAll('#quick-results .search-result').length>0);
    const modalAudit = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
    assert.deepEqual(modalAudit.violations.map(v=>v.id),[], 'search dialog accessibility');
    await page.keyboard.press('Escape');
    await page.waitForFunction(()=>!document.querySelector('#search-dialog').open);
    await page.locator('#save-wisdom').click();
    assert.equal(await page.locator('#save-wisdom').getAttribute('aria-pressed'),'true');
    await page.reload();
    assert.equal(await page.locator('#save-wisdom').getAttribute('aria-pressed'),'true');
    assert.equal(await page.locator('#saved-list .saved-item').count(),1);
    await page.locator('#saved-list button').click();
    assert.equal(await page.locator('#saved-section').isVisible(),false);
    const before = await page.locator('#wisdom-content blockquote').textContent();
    await page.locator('#next-wisdom').click();
    assert.notEqual(await page.locator('#wisdom-content blockquote').textContent(),before);
    await page.evaluate(() => {
      Object.defineProperty(navigator,'share',{value:undefined,configurable:true});
      Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>window.sharedText=text},configurable:true});
    });
    await page.locator('#share-wisdom').click();
    assert.match(await page.evaluate(()=>window.sharedText),/#wisdom-4/);
    await page.goto(base+'/search.html?q=knowledge');
    await page.waitForFunction(()=>document.querySelectorAll('#results .search-result').length>0);
    await page.locator('[data-kind="letter"]').click();
    await page.waitForFunction(()=>!document.querySelector('#status').textContent.includes('Searching'));
    const types = await page.locator('#results small').allTextContents();
    assert(types.every(type=>type==='Letter'));
    await page.locator('[data-kind="all"]').click();
    await page.locator('#q').fill('zzzzzznonexistent');
    await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('No matches'));
    await page.locator('#q').fill('عِلْم');
    await page.locator('#searchForm button').click();
    await page.waitForFunction(()=>document.querySelectorAll('#results .search-result').length>0);
    await page.locator('[data-lang="fa"]').click();
    await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('نتیجه'));
    const searchAudit = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
    assert.deepEqual(searchAudit.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})),[], 'search page accessibility');
    await page.goto(base+'/quote/1.html#wisdom-5');
    assert.equal(await page.locator('#wisdom-5').count(),1);
    assert.deepEqual(errors,[],'No JS runtime errors');
    await context.close();
    const noJS = await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
    const fallback = await noJS.newPage();await fallback.goto(base);
    assert.equal(await fallback.locator('.collection-card').count(),3);
    assert.equal(await fallback.locator('.collection-card').first().evaluate(el=>getComputedStyle(el).opacity),'1');
    await noJS.close();
    console.log('PASS: FA/EN, 5 viewport sizes, accessibility, menu, search, save/remove persistence, wisdom rotation, share, deep links, no-JS fallback.');
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
