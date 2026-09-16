# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary readers include:

- Persian speakers studying or consulting Nahj al-Balagha
- English readers seeking access to the same text
- People reading short sayings (hikam) for daily reflection
- Readers using the site as a structured reference (sermons, letters, wisdoms)

Default experience is Persian (FA), RTL; English (EN) is a first-class alternate language, not a secondary afterthought.

## Product Purpose

**نهج البلاغه | Imam Ali** (`imamali.xyz`) is a free static website that presents Nahj al-Balagha — sermons (خطبه‌ها), letters (نامه‌ها), and short sayings (کلمات قصار / hikam) — with Persian and English translations so readers can browse, read, and return to the text without an app or account.

Success means a reader can find the right section quickly, read in their language, and trust that the structure and presentation stay faithful to the classical three-part work compiled by al-Sharif al-Radi (سید رضی).

## Positioning

A complete, bilingual, structured Nahj al-Balagha reading site — not a generic Islamic-quote feed. Content is organized as the book is traditionally organized (sermons, letters, ~480 short sayings), with FA/EN switching and a dedicated domain (`imamali.xyz`).

## Operating Context

- Static site opened in a browser (desktop and mobile)
- Language choice FA/EN persisted in `localStorage` (`nahj-lang`)
- Deployed via GitHub Pages with custom domain `imamali.xyz`
- Main entry paths: home → sermons / letters / wisdoms / about; wisdoms paginated across `quote/*.html`

## Capabilities and Constraints

**Confirmed capabilities**

- Browse sermons (`khutbah.html`), letters (`rasail.html`), and short sayings (`quote/*.html`, `hikam.html`)
- Bilingual UI and translations (FA / EN)
- About page explaining the work and its three parts
- SEO basics (`sitemap.xml`, `robots.txt`, canonical URLs)

**Confirmed constraints**

- Static HTML/CSS (no app backend); keep the site readable and deployable as static files
- Preserve the classical three-part structure and terminology (خطبه‌ها / نامه‌ها / کلمات قصار)
- Do not invent sermons, letters, sayings, attributions, or historical claims
- Brand name: **نهج البلاغه** / Nahj al-Balagha; site identity tied to **imamali.xyz**

**Open / undecided**

- Preferred scholarly edition or translation sources for disputed wording (not specified)
- Formal accessibility standard target (e.g. WCAG level) not yet set by the product owner

## Brand Commitments

- Product name: نهج البلاغه (Nahj al-Balagha — “the path of eloquence”)
- Domain / site: imamali.xyz
- Voice: respectful, clear, suitable for sacred literary text; bilingual without diluting either language
- Incumbent UI identity exists in code (navy / gold / cream, Amiri + Vazirmatn); visual system documentation is a separate step (`/impeccable document`), not redefined here

## Evidence on Hand

- Full site HTML: `index.html`, `khutbah.html`, `rasail.html`, `about.html`, `quote/*.html`, `letter/*.html`, and related detail pages
- Shared styles: `style.css`
- Project overview: `README.md`
- Deploy/SEO: `CNAME`, `sitemap.xml`, `robots.txt`

Future work must not fabricate testimonials, scholarly endorsements, licensing claims, or content that is not present in the repository.

## Product Principles

1. **Faithfulness first** — structure and claims follow the classical Nahj al-Balagha; never invent text or attribution.
2. **Bilingual by design** — FA and EN are both real reading modes; default remains FA/RTL.
3. **Findability over novelty** — readers should reach the right sermon, letter, or saying with minimal friction.
4. **Static and durable** — keep the site simple to host, archive, and maintain as HTML/CSS.
5. **Respectful presentation** — tone and framing suit a major Islamic literary work.

## Accessibility & Inclusion

No product-owner-mandated standard yet. Practical needs already implied by the audience: clear typography for Arabic/Persian reading, usable mobile layouts, keyboard-accessible controls, and sufficient contrast for body text. Formal WCAG target remains open.
