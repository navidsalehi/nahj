---
name: نهج البلاغه | Imam Ali
description: Bilingual Nahj al-Balagha reading site — navy frame, parchment page, scarce lamp gold
colors:
  manuscript-navy: "#0b1526"
  manuscript-navy-2: "#111d33"
  manuscript-navy-3: "#1a2a45"
  lamp-gold: "#c9a84c"
  lamp-gold-light: "#e8d5a3"
  lamp-gold-dim: "rgba(201, 168, 76, 0.15)"
  parchment-cream: "#f7f4ef"
  paper-white: "#ffffff"
  near-black-ink: "#1a1a1a"
  soft-charcoal: "#3d4654"
  margin-slate: "#4a5568"
  hairline-border: "#e2e8f0"
typography:
  display:
    fontFamily: "Amiri, Georgia, serif"
    fontSize: "clamp(2.1rem, 5vw, 3.1rem)"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "normal"
  headline:
    fontFamily: "Vazirmatn, system-ui, sans-serif"
    fontSize: "1.4rem"
    fontWeight: 700
    lineHeight: 1.45
    letterSpacing: "normal"
  title:
    fontFamily: "Vazirmatn, system-ui, sans-serif"
    fontSize: "1.2rem"
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: "normal"
  body:
    fontFamily: "Vazirmatn, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.8
    letterSpacing: "normal"
  arabic-body:
    fontFamily: "Amiri, Georgia, serif"
    fontSize: "1.2rem"
    fontWeight: 400
    lineHeight: 2
    letterSpacing: "normal"
  label:
    fontFamily: "Vazirmatn, system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.04em"
rounded:
  sm: "6px"
  md: "8px"
  control: "10px"
  lg: "14px"
  xl: "16px"
  pill: "999px"
spacing:
  xs: "0.35rem"
  sm: "0.75rem"
  md: "1.25rem"
  lg: "1.85rem"
  xl: "3rem"
  container: "1100px"
  reading: "40rem"
  letter: "720px"
components:
  button-primary:
    backgroundColor: "{colors.lamp-gold}"
    textColor: "{colors.manuscript-navy}"
    rounded: "{rounded.control}"
    padding: "0.8rem 1.55rem"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.lamp-gold-light}"
    textColor: "{colors.manuscript-navy}"
    rounded: "{rounded.control}"
    padding: "0.8rem 1.55rem"
  button-chrome:
    backgroundColor: "{colors.manuscript-navy}"
    textColor: "{colors.lamp-gold-light}"
    rounded: "{rounded.control}"
    padding: "0.65rem 1rem"
  card-surface:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.manuscript-navy}"
    rounded: "{rounded.lg}"
    padding: "1.35rem 1.3rem"
  chip-selected:
    backgroundColor: "{colors.lamp-gold}"
    textColor: "{colors.manuscript-navy}"
    rounded: "{rounded.pill}"
    padding: "0.35rem 0.7rem"
  chip-idle:
    backgroundColor: "transparent"
    textColor: "rgba(255,255,255,0.72)"
    rounded: "{rounded.pill}"
    padding: "0.35rem 0.7rem"
  input-search:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.near-black-ink}"
    rounded: "{rounded.control}"
    padding: "0.75rem 1rem"
  nav-link:
    backgroundColor: "transparent"
    textColor: "rgba(255,255,255,0.75)"
    rounded: "{rounded.md}"
    padding: "0.45rem 0.85rem"
  nav-link-active:
    backgroundColor: "rgba(201,168,76,0.12)"
    textColor: "{colors.lamp-gold}"
    rounded: "{rounded.md}"
    padding: "0.45rem 0.85rem"
---

# Design System: نهج البلاغه | Imam Ali

## Overview

**Creative North Star: "The Gold-Lamped Lectern"**

The site reads like a quiet lectern under a single warm lamp: a dark Manuscript Navy frame (topbar and footer) holds a soft Parchment Cream page, and Lamp Gold appears only where attention or action is required. Personality is calm and dignified—built for long bilingual reading, not marketing spectacle. Density stays open: generous line-height for Arabic and Persian, clear section cards, and a measured 1100px content column.

Form language is refined and restrained—paper-white surfaces, soft radii, calm hairline borders. Gold is scarce accent, never wallpaper. Default reading direction is RTL (FA); LTR (EN) is a first-class mirror, not a bolted-on theme.

Confirmed visual anti-references: generic AI “cream + terracotta serif landing” kits, and dashboard / SaaS chrome. External stock library imagery may appear in heroes today; it is presentation debt, not identity.

**Key Characteristics:**
- Navy chrome + parchment page + scarce lamp gold
- Amiri for Arabic literary text; Vazirmatn for UI and Persian body
- Soft radii; prefer border/tone over heavy shadow
- Bilingual FA/EN with RTL-first defaults
- Static HTML/CSS patterns reusable across list, quote, and letter pages

## Colors

A two-voice palette: deep ink for structure, warm lamp for emphasis, parchment for the reading field.

### Primary
- **Manuscript Navy** (`#0b1526`): Chrome (topbar, footer), headings, links at rest, Arabic text color, primary reading ink on light surfaces. Steps `--navy-2` (`#111d33`) and `--navy-3` (`#1a2a45`) deepen panels (mobile nav) without introducing a second hue.
- **Lamp Gold** (`#c9a84c`): Primary action and focus accent—CTA fills, brand mark, active nav, pagination on-state, focus outline. Light twin **Lamp Gold Light** (`#e8d5a3`) for brand wordmark and hero titles on navy. Dim wash **Lamp Gold Dim** (`rgba(201,168,76,0.15)`) for icon wells and badges.

### Neutral
- **Parchment Cream** (`#f7f4ef`): Page background—the reading room paper. Incumbent and intentional; pair always with navy/gold, never with terracotta fashion kits.
- **Paper White** (`#ffffff`): Elevated content surfaces (cards, quote boxes, inputs).
- **Near-Black Ink** (`#1a1a1a`): Default body text on cream.
- **Soft Charcoal** (`#3d4654`): Translations and secondary prose.
- **Margin Slate** (`#4a5568`): Captions, metadata, quieter secondary copy (WCAG-safe on white).
- **Hairline Border** (`#e2e8f0`): Card and field strokes.

### Named Rules
**The Scarce Lamp Rule.** Lamp Gold occupies a small fraction of any screen. If gold is everywhere, the lectern has no light—only glare.

**The Parchment Pairing Rule.** Cream is allowed only as the page ground paired with Manuscript Navy and Lamp Gold. Never restyle cream into a warm terracotta/serif “AI landing” lookalike.

## Typography

**Display Font:** Amiri (with Georgia, serif)  
**Body Font:** Vazirmatn (with system-ui, sans-serif)  
**EN translation:** system-ui / -apple-system for LTR translation blocks

**Character:** Amiri carries the classical Arabic voice of the text; Vazirmatn keeps UI and Persian body clear and modern without competing with the literary face.

### Hierarchy
- **Display** (Amiri 700, `clamp(2.1rem, 5vw, 3.1rem)`, lh 1.25): Hero and page-hero titles; gold-light on navy photography.
- **Headline** (Vazirmatn 700, ~1.4rem): Section headings (e.g. selected sayings).
- **Title** (Vazirmatn 700, ~1.2rem): Card and list titles.
- **Arabic body** (Amiri 400, ~1.15–1.4rem, lh ~1.95–2.2): Sermons, letters, hikam Arabic. Prefer generous measure and line-height.
- **Body** (Vazirmatn 400, 16px / 1rem, lh 1.8): UI chrome and Persian prose; about measure ~40rem.
- **Label** (Vazirmatn 600–700, 0.72–0.8rem): Badges, numbers, functional section labels on letter blocks. Not a marketing eyebrow.

### Named Rules
**The Two-Voice Rule.** Arabic literary content speaks in Amiri; chrome and Persian UI speak in Vazirmatn. Do not reverse them for decoration.

## Layout

Centered content column at **1100px** max width with **1.25rem** side padding. Letter reader tightens to **720px**; about prose to **~40rem**. Topbar is sticky, **64px** tall. Home section cards and quote rows use a **3-column** grid collapsing to **1 column** at **720px**. Hikam grids become **2 columns** from **768px**. Mobile navigation collapses below **800px**.

Rhythm: group related content tightly; separate major sections generously (≈1.25–3.5rem). Home cards may overlap the hero with a slight negative margin—keep that as a home-only bridge, not a global pattern.

RTL is default; mirrored LTR for `lang-en` must preserve the same spacing scale and touch targets (≥44px for primary controls).

## Elevation & Depth

**Preferred philosophy (confirmed): flatter.** Prefer hairline borders and tonal washes over stacked shadows. Soft shadows exist in the current build as ambient card lift; future screens should lean on **border + paper-white on parchment** first, and use shadow sparingly.

Where depth appears today: navy gradient over hero imagery; white cards on cream; gold-dim icon wells; interaction lift on hover (small translateY + slightly deeper shadow).

### Shadow Vocabulary (incumbent; use sparingly)
- **Card ambient** (`0 4px 24px rgba(11, 21, 38, 0.08)`): Default white card rest state—optional; borders can replace.
- **Card hover** (`0 8px 32px rgba(11, 21, 38, 0.12)` or `0 8px 28px …`): Interaction only.
- **Chrome** (`0 2px 12px rgba(0,0,0,0.15)`): Sticky topbar separation.
- **Focus** (`0 0 0 3px rgba(201, 168, 76, 0.45)` + 2px gold outline): Keyboard focus, not decoration.

### Named Rules
**The Quiet Surface Rule.** Default surfaces are flat paper on parchment. Shadows answer interaction or sticky chrome—they are not the identity.

## Shapes

Soft, literary, never sharp-brutalist and never fully pill-everything. **14px** (`--radius`) is the default card corner; **10px** for controls (CTA, inputs, tools); **8px** for nav chips and pagination; **6px** for small badges; **999px** only for true pills (language switch, filter chips, letter chip). Icon wells use ~12px.

Borders are 1px hairline (`#e2e8f0`) or subtle gold-tinted strokes on interactive hover—not thick accent bars on the inline-start edge.

## Components

### Buttons
Refined and restrained—paper and gold, not glossy SaaS.

- **Shape:** Gently curved control radius (10px)
- **Primary (hero CTA):** Lamp Gold fill, Manuscript Navy text, min-height 44px; hover → Lamp Gold Light; optional 1px lift
- **Chrome / letter-nav primary:** Manuscript Navy fill, Lamp Gold Light text
- **Tool / secondary:** White fill, hairline border, Soft Charcoal text; hover → gold-dim wash + gold border
- **Focus:** Gold outline + focus ring token on all interactive controls

### Chips
- **Language switch:** Pill on navy chrome; selected = Lamp Gold fill / navy text
- **Filters:** Pill; selected should match CSS `.on` (navy fill / gold-light text)—keep HTML class names aligned with CSS

### Cards / Containers
- **Corner Style:** 14px default; letter content blocks up to 16px
- **Background:** Paper White on Parchment Cream
- **Shadow Strategy:** Prefer border; ambient shadow optional per Quiet Surface Rule
- **Border:** 1px hairline; hover may tint toward gold
- **Internal Padding:** ~1.1–1.85rem
- **Section cards:** Full-card links with gold-dim SVG icon well (stroke icons, not emoji)

### Inputs / Fields
- **Style:** White field, hairline border, 10px radius, Vazirmatn
- **Focus:** Border shifts to Lamp Gold (no loud glow beyond the shared focus ring)

### Navigation
- Sticky Manuscript Navy topbar; brand with Amiri «ن» mark on Lamp Gold tile
- Links: muted white at rest; Lamp Gold + gold-dim wash when active/hover
- Mobile: hamburger as CSS bars (not glyph characters); panel uses navy-2

### Quote / Hikam / Letter (signature reading surfaces)
- **Quote box:** Amiri Arabic blockquote + muted Vazirmatn caption
- **Hikam card:** Gold number, Amiri Arabic, dashed divider, Soft Charcoal translation
- **Letter shell:** Narrow column, navy chip, labeled Arabic/translation blocks, prev/next nav

## Do's and Don'ts

### Do:
- **Do** keep Manuscript Navy / Lamp Gold / Parchment Cream as the only core triad.
- **Do** set Arabic literary text in Amiri and UI/Persian in Vazirmatn.
- **Do** design FA RTL first; mirror carefully for EN LTR.
- **Do** prefer hairline borders and tonal washes over heavy drop shadows.
- **Do** use Lamp Gold for primary action and focus—and rarely elsewhere.
- **Do** use consistent stroke SVG icons in gold-dim wells.

### Don't:
- **Don't** drift into generic cream + terracotta + display-serif “AI landing” aesthetics.
- **Don't** introduce dashboard/SaaS chrome (dense metric cards, purple gradients, neon glow).
- **Don't** use emoji or Unicode symbols as the icon system (including ☰ / 🔊 as permanent UI).
- **Don't** invent kickers/eyebrows above headings; headings carry their own weight.
- **Don't** invent sermons, letters, sayings, or attributions for visual filler.
- **Don't** flood screens with gold or stack nested cards for decoration.

## September 2026 homepage refresh

The homepage now extends the navy / scarce gold / parchment system into a responsive editorial layout. This is a library, not a SaaS landing page: there are no invented usage metrics, endorsements, or textual attributions.

- **Composition:** asymmetric, RTL-first split hero with an arched decorative book image; three clear collection doorways; a quiet, dark featured-wisdom panel; subject shortcuts; an understated reading CTA.
- **Type:** locally hosted Amiri for Arabic/Persian display and literary passages, Vazirmatn for UI, and Cormorant Garamond for the English editorial hero. English layout mirrors structurally; Arabic quotations keep `lang="ar" dir="rtl"`.
- **Motion:** short entrance and one-time section reveals, restrained hover feedback, and a scroll progress line. No scroll hijacking, automatic quotation rotation, or mandatory animation. Reduced-motion preferences turn motion off, and content remains visible without JavaScript.
- **Useful interactions:** search dialog with native focus containment, Escape dismissal, focus restoration, keyboard shortcuts, and links to full results; manual featured-wisdom rotation; local saved items with a visible saved list; native share or clipboard fallback.
- **Responsive behavior:** three-column collections on large screens, stacked cards on phones; the hero stacks below 580px; navigation becomes a disclosure at 800px. Topics reduce to two columns on narrow phones.
- **Assets:** the hero is an 88 KB decorative WebP. Font files and licenses are local; the roughly 256 KB search index loads only when a query is made.

Design references at the pattern level: Apple's editorial spacing and image-led hierarchy, Linear's restrained interaction feedback, and Quran.com's emphasis on findable, readable religious texts. This is an original implementation, not a clone or an affiliation with those products.
