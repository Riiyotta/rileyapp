Source: https://rileyapp.com/

# Riley marketing landing pages: clone spec

Recon date: 2026-10-13. Measured live with Playwright (Chromium) at 1440x900, 1280x800, 768x1024 and 390x844. Values are computed styles or getBoundingClientRect results unless marked **UNVERIFIED**. This file only specs what is **not** already in `CLONE_SPEC.md` (homepage). Section numbers like "§9.2" refer to `CLONE_SPEC.md`.

Raw dumps: `.playwright-mcp/pricing-hero-1440.json` (full DOM and computed-style walk of the pricing hero), `.playwright-mcp/pricing-hero-svgs.json` (inline SVG markup and matching CSS rules), `.playwright-mcp/notfound-1280.png` (full-page screenshot of the 404 template).

---

## 0. Headline finding: 8 of the 9 routes are soft-404s

All eight sitemap landing routes return **HTTP 200** but render Next.js `notFound()`. The RSC payload contains `5:E{"digest":"NEXT_HTTP_ERROR_FALLBACK;404"}` and the page sets `<meta name="robots" content="noindex">`. The `[slug]` catch-all route renders them. Their Storyblok stories are evidently unpublished or deleted. All eight show the **same** "Oops! This page is playing peekaboo..." 404 template. There is no per-route content.

| Route | In sitemap | HTTP | Renders | Verified |
|---|---|---|---|---|
| /baby-tracker | yes | 200 | 404 template | browser plus RSC fetch |
| /sleep-tracker | yes | 200 | 404 template | browser plus RSC fetch |
| /sleep-training | yes | 200 | 404 template | browser (390/768/1280) plus RSC |
| /sleep-regression | yes | 200 | 404 template | RSC fetch |
| /all-in-one | yes | 200 | 404 template | RSC fetch |
| /your-babys-sleep-simplified | yes | 200 | 404 template | RSC fetch |
| /product-hunt | yes | 200 | 404 template | RSC fetch |
| /give-the-gift | yes | 200 | 404 template | browser plus RSC fetch |
| **/pricing** | **no** | 200, no redirect | **real page** | browser at all 4 widths |

The same holds for `www.rileyapp.com/<route>`. Wayback Machine captures were checked too. /baby-tracker and /give-the-gift (2025-12-07) contain the same 404 digest, and /product-hunt (2025-05-17) is titled "Page Not Found | Riley - Riley". So no historical landing-page design exists to clone either.

**Implication for Build:** do not create 8 separate landing pages. Replace the placeholder `src/pages/NotFound.jsx` body with the measured `NotFoundPage` template (§2), and let these 8 slugs, plus any unknown path, fall through to it. Only `/pricing` needs a new page composition.

---

## 1. REUSE MATRIX

### 1.1 /baby-tracker, /sleep-tracker, /sleep-training, /sleep-regression, /all-in-one, /your-babys-sleep-simplified, /product-hunt, /give-the-gift (identical)
DOM order: `body` > `AnnouncementBar` div > `header` > 404 div > `footer`. There is no page wrapper div and no hero wrapper.
1. `REUSE AnnouncementBar`: identical (same aside classes, inline bg #d7befc, link to /pricing). Hidden <992.
2. `REUSE SiteHeader`: identical classes, sticky behaviour (M2: fixed after scrollY>54, 80px spacer, shadow-md, blur 12px) and load fade. It sits directly on the latte body, with no hero clouds behind it. Live quirk: the header wordmark `<img>` never finishes loading on the 404 route (`complete:false`, `naturalWidth 0`; the `_next/image ... w=96` request never resolves), so the logo slot is blank on the live 404. Treat that as a live bug and render the logo normally.
3. `NEW NotFoundPage` (the "peekaboo" block, §2).
4. `REUSE SiteFooter`: identical (493.6 @1440, 553.6 @768, 713.4 @390).

### 1.2 /pricing
DOM order: `body` > `AnnouncementBar` div > `div.relative.flex.flex-col.items-start.overflow-hidden` (page wrapper, holds everything below):
1. `REUSE AnnouncementBar`: identical.
2. `REUSE SiteHeader`: identical. Standalone, as the first child of the page wrapper, not inside the Hero wrapper.
3. `NEW PricingHero` (§3). Internally it reuses `HeroParallaxClouds`. Props needed are in §1.4.
4. `REUSE Testimonials`: identical text, 5 slides, avatars, "Join the club" CTA. Heights match the homepage (1058 / 1125.6 / 816 / 1076.6).
5. `REUSE GradientBand` **without FeatureCards**: the same radial-gradient wrapper (`flex flex-col items-center gap-12 self-stretch px-4 py-11 lg:px-8`, padding 44px 32px, gap 48) containing **only** `ComparisonTable`. The table is identical: same eyebrow, H2, prose, 5x7 check matrix, "Join Riley—early, easy, free" CTA. Wrapper height 1250.2 @1440/1280, 1065.4 @768, 1176.6 @390.
6. `REUSE FaqClouds`: identical (same 5 questions, portraits 4/5/3/2/6.png, riley-up.svg, "Learn More" → /pricing). Height 900 / 900 / 1100 / 1100.
7. `REUSE FinalCta`: identical ("We are raising a generation / of confident parents.", "Get support that gets you", background-clouds(1).svg, mascots.svg). Heights 708 / 786 / 440 / 536.
8. `REUSE SiteFooter`: identical.

Not present on /pricing: Hero/HeroContent, PressMarquee, PersonalizationMarquee, Superpowers, Featurette, ClinicalBoard, HowRileyWorks, FeatureCards, BlogTeaser.

### 1.3 De-duplicated NEW components
| Component | Used on | Spec |
|---|---|---|
| `NotFoundPage` (replace the body of `src/pages/NotFound.jsx`) | all 8 landing slugs plus the catch-all | §2 |
| `PricingHero` (with sub-component `PlanCard`, used x2) | /pricing | §3 |

No shared "landing hero template" is needed: none of the landing pages has content.

### 1.4 Prop or parameter changes to existing components (needed for /pricing)
- **`GradientBand`**: add a prop such as `showFeatureCards` (default `true`). /pricing renders the wrapper with only `<ComparisonTable/>`.
- **`HeroParallaxClouds`**: reused verbatim for the cloud layers (same 4 layers, same cloud SVGs `hero-cloud-1..4.svg` byte-identical by path and gradient id, same classes, same float animations and delays, same parallax ranges 20/35/50/100% plus scale .8→1.2 on layer 4). Differences on /pricing:
  - Layer 1's banner has **no `bg-hero` background**. All four layer wrappers are plain `absolute inset-0` inside one parent `div.pointer-events-none.absolute.inset-0.-z-20.opacity-70`, so the whole cloud stack renders at **opacity .7**.
  - The parallax progress element is the PricingHero `section`. Measured `p = clamp(scrollY / (sectionTop + sectionHeight), 0, 1)` = scrollY / 1233.7 @1440 (134.4 + 1099.3). At scrollY 300: L1 -4.863%, L2 -8.511%, L3 -12.159%, L4 -24.317% scale .8973. At scrollY 1300 everything is complete (-20 / -35 / -50 / -100%, scale 1.2). This is the same formula as the homepage, with a different target element. The expanded insets also derive from the section height: L1 top -219.859 (20% of 1099.3), L2 -384.754, L3 -549.648.
  - So the component needs props like `bannerClassName` (or `withBg={false}`) and a ref or target for the progress container.
- **`Button`**: the pricing CTA needs (a) a trailing icon slot (`button-arrow.svg` 16x17 after the label inside the inner span, gap 8) and (b) extra classes `w-full sm:w-full max-w-[24rem] mx-auto min-h-[56px] text-base sm:text-lg`. That gives **18px/28px** text and a 384x**60** button at ≥640, and 16px/24px and 326x56 at <640. Colours and JS hover/active are unchanged (#5934C5 → #7A55FD → #5A20E1, 300ms cubic-bezier(.4,0,.2,1)).
- `SiteHeader`, `AnnouncementBar`, `Testimonials`, `ComparisonTable`, `FaqClouds`, `FinalCta`, `SiteFooter`: no prop changes.

---

## 2. NEW `NotFoundPage` ("peekaboo" 404 template)

### 2.1 Structure and classes (original)
```
div.mx-auto.flex.min-h-[500px].w-full.flex-col.items-center.gap-6.px-6.pt-12.text-center.xl:min-h-[850px]
├─ h3.text-text-primary.font-serif.text-4xl.font-medium.xl:text-6xl   "Oops! This page is playing peekaboo... and it's REALLY good at it."
├─ p.font-book.text-text-primary.max-w-[700px].font-serif.text-base.xl:text-xl   "Looks like this link went on a nap and forgot to wake up."
├─ a[href="/"].ext-white.text-brand-500.hover:text-brand-600.flex.flex-row.items-center.gap-3   "Go back" + span.text-lg "›"
└─ img.-z-100.bottom-0.left-0.w-full.scale-105   (Next <Image>, width=1440 height=561, loading=lazy, alt="" UNVERIFIED)
```
Note: `ext-white` (typo), `text-brand-500`, `hover:text-brand-600` and `font-book` are **not defined** in the original CSS. The link therefore inherits **#0a0a0a** (`oklch(14.5% 0 0)`) and has **no hover colour change** and no underline. `bottom-0 left-0` have no effect because the img is `position: static`. It sits in normal flow as the last flex item.

### 2.2 Measured layout
| | 1440 | 1280 | 768 | 390 |
|---|---|---|---|---|
| Container y / h | 134.4 / **850** (xl:min-h) | 134.4 / 850 | 80 / **532.5** (content > min 500) | 80 / **500** (min-h) |
| Container padding / gap | 48px 24px 0 / 24 | same | same | same |
| h3 box | 24, 182.4, 1392x120 (2 lines) | 1232x120 (2 lines) | 720x80 (2 lines) | 342x160 (4 lines) |
| p box | 485.1x28 centered (x 477.4) | 485.1x28 | 388.1x24 | 342x48 (2 lines) |
| a box | 78.3x28 (x 680.9, y 378.4) | 78.3x28 | 78.3x28 | 78.3x28 |
| img layout box → rendered (scale 1.05) | 1392 wide → **1461.6x569.4** at x -10.8, y 416.8 | 1293.6x504 at x -6.8 | 756x294.5 at x 6 | 359.1x139.9 at x 15.5 |

The image's layout width = container width minus 48px padding. Its height comes from the 1440:561 aspect. `scale:1.05` (Tailwind v4 `scale` property, not `transform`) enlarges it about its centre. At 1440 it overflows the container bottom by 1.8px (ends at 986.2, footer starts at 984.4). At ≥1280 the container is fixed at 850 tall, so there is about 62px of empty latte between the image bottom and the footer at 1280.

AnnouncementBar is present ≥992 only. At 768 and 390 the header is at y 0.

### 2.3 Typography and colour (computed)
| Role | ≥1280 (`xl`) | <1280 (768/390 measured) |
|---|---|---|
| h3 | Recoleta (`"serif"`) **60px/60px**, weight **500** (only a 400 face exists; Chrome does not synthesise bold below 600, so it renders as regular), #2e2a42, centred | Recoleta **36px/40px**, w500 |
| p | Recoleta **20px/28px**, w400, #2e2a42, max-w 700 | Recoleta **16px/24px** |
| a "Go back" | Cadiz Regular 16px/24px, **#0a0a0a**, flex, gap 12 | same |
| span "›" | Cadiz Regular 18px/28px | same |

Tailwind v4 defaults behind these: `text-4xl` = 2.25rem / lh 2.5rem; `text-6xl` = 3.75rem / lh 1; `text-xl` = 1.25rem / lh 1.75rem; `text-base` = 1rem / 1.5rem; `text-lg` = 1.125rem / 1.75rem. Tailwind v3 has the same defaults.

Page bg: body latte **#f9f5f1**. The img has inline `color: transparent`.

### 2.4 Asset
- `public/assets/shared/background.bc1c0c29.svg`: original `/_next/static/media/background.bc1c0c29.svg`, **1440x561**, 29.7 KB. Illustration: a purple "worrier"-style cloud mascot (hand on head, frown) standing on rolling rainbow-gradient ribbon loops over a pale blue hill. It contains 6 `<foreignObject>` elements (backdrop-blur divs), 3 linearGradients and 7 clipPaths. Render it with `<img>` like the original. Do not inline it.

### 2.5 Motion
None on the 404 block: no transitions, animations or observers (all computed `transition` values are the default `all 0s`). The header keeps its own load fade (M1/M1b) and sticky behaviour (M2).

### 2.6 Page meta (404 routes)
- `<title>` **Riley – Baby Tracker & Child Development Expert** (same as homepage)
- meta description: "Riley learns and grows with your family, offering personalized, data-backed guidance so you're ready for anything life—or your kids—throw your way."
- `<meta name="robots" content="noindex">`

---

## 3. NEW `PricingHero` (/pricing section 1)

### 3.1 Structure (original classes)
```
section.relative.isolate.w-full.overflow-x-hidden                         (1440x1099.3 @1440, y 134.4)
├─ div.bg-pricing-radial.absolute.inset-0.-z-40                           radial bg
├─ div.pointer-events-none.absolute.inset-0.-z-20.opacity-70              HeroParallaxClouds (4 layers, see §1.4)
└─ div.relative.z-10
   └─ div.py-8.sm:py-12.lg:py-16
      ├─ div.flex.flex-col.items-center.gap-2.mb-8.sm:mb-12.px-4
      │  └─ p.font-sans-regular.text-text-primary.mobile-h4.lg:text-[1.25rem].text-center   "Parenting Made Simple"
      └─ div.w-full.max-w-[80rem].mx-auto.px-4.sm:px-6.lg:px-14
         ├─ div.text-center.mb-8.sm:mb-12
         │  └─ h1.mobile-h1.lg:desktop-h1.text-text-primary.font-serif.mb-4   "Expert Guidance,<br>Tailored To Your Family"
         ├─ div.grid.md:grid-cols-2.gap-6.sm:gap-8.max-w-[56rem].mx-auto.mb-8.sm:mb-12
         │  ├─ PlanCard "Riley Plus+"
         │  └─ PlanCard "Riley Basic"
         └─ div.text-center.px-4.sm:px-0
            └─ Button "Get Started For Free" + arrow icon
```

### 3.2 Background
- `.bg-pricing-radial`: `background-image: radial-gradient(45.01% 50.02% at 50% 52.71%, #ff914d 0, #f9f5f1 100%)` (`--Primary-Tangerine` → `--Primary-Latte`). It covers the whole section (absolute inset 0, z -40).
- Clouds: see §1.4. The cloud stack is at z -20 with opacity .7, behind the content (z 10). The section clips horizontally (`overflow-x:hidden`, which computes to `hidden auto`).

### 3.3 Layout per breakpoint
| | 1440 | 1280 | 768 | 390 |
|---|---|---|---|---|
| Section height | **1099.3** | 1099.3 | **1043.3** | **1471.8** |
| Vertical padding (`py-8 sm:py-12 lg:py-16`) | 64 | 64 | 48 | 32 |
| Eyebrow row margin-bottom | 48 | 48 | 48 | 32 |
| Content container | max-w 1280, padding-x **56** (x 80 → 1360) | x 0, w 1280, padding-x 56 | padding-x **24** | padding-x **16** |
| H1 box | 1168x144 (2 lines) | 1168x144 | 720x96 (2 lines) | 358x144 (3 lines: "Expert Guidance," / "Tailored To Your" / "Family") |
| H1 block margin-bottom (`mb-8 sm:mb-12`) | 48 | 48 | 48 | 32 |
| Grid | 2 cols **432 + 432**, gap **32**, max-w 896, x 272 | x 192 | 2 cols **344 + 344**, gap 32 | 1 col 358, gap **24** |
| Card size | 432x**602.5** (both equal, grid stretch) | same | 344x626.5 | 358x551 (Plus) / 358x516 (Basic) |
| Grid margin-bottom | 48 | 48 | 48 | 32 |
| CTA | 384x**60**, centred (x 528) | x 448 | 384x60 (x 192) | **326x56** (wrapper px-4) |

Element y positions @1440: eyebrow 198.4; h1 267.2; grid 459.2; CTA 1109.7; section bottom 1233.7.

### 3.4 Typography (computed)
| Role | ≥992 | 768 | 390 |
|---|---|---|---|
| Eyebrow "Parenting Made Simple" | Cadiz Regular **20px/20.8px**, #2e2a42, centred (210.4x20.8) | Recoleta 16px/20.8px (the unlayered `.mobile-h4` rule swaps the family to serif below 992) | Recoleta 16px/20.8px (163.2 wide) |
| H1 | Recoleta **64px/72px**, #2e2a42, centred, mb 16 (the unlayered `h1` rule beats `lg:desktop-h1`) | Recoleta 40px/48px | Recoleta 40px/48px |
| Plan name h3 (`text-[28px] sm:text-[32px]`) | Recoleta **32px/48px**, #2e2a42, mb 8 | 32/48 | **28px/42px** |
| Plan description p (`text-sm sm:text-base`) | Cadiz Regular **16px/24px**, `rgba(46,42,66,.7)`, mb 8. Box height 30.5 because of the inline avatars | 16/24 (wraps to 2 lines, 54.5 tall @768) | 14px/20px (box 25) |
| Green tagline (`text-sea-green-100 font-sans-semibold text-sm`) | Cadiz **SemiBold** face 14px/20px (fw 400 computed), **#4ca67e** | same | same |
| Feature item span | Cadiz Regular **14px/20px**, #2e2a42 | same | same |
| "Starting at" / "Billed monthly…" / "Available on:" | Cadiz Regular 14px/20px, `rgba(46,42,66,.7)` | same | same |
| Price "$9.99" / "Free" | Recoleta **32px/48px**, #2e2a42 | 32/48 | 28px/42px |
| "/ month" span | Recoleta **16px/24px**, `rgba(46,42,66,.7)` (inline after "$9.99 ") | 16/24 | 14px/21px |
| CTA label | Cadiz Bold face **18px/28px** (≥640), white | 18/28 | **16px/24px** |

### 3.5 PlanCard
Card: `div.bg-white.rounded-2xl.sm:rounded-3xl.border.border-latte-125.p-6.sm:p-8`. bg **#ffffff**, border **1px solid #c7c3c0** (`latte-125`), radius **24** (≥640) / **16** (<640), padding **32** (≥640) / **24** (<640). **No shadow, no hover state.** Content box 366 wide @1440.

Inner blocks, in order:
1. `div.mb-6` (mb 24): header
   - h3 plan name.
   - p description + `span.inline-flex.items-center.gap-0.5.ml-2` (ml 8, gap 2) holding avatar `img.w-5.h-5.sm:w-6.sm:h-6` (**24x24** ≥640, **20x20** <640, alt "Riley avatar", vertically centred on the text line).
   - p green tagline.
2. `div.mb-6.sm:mb-8` (mb 32 ≥640, 24 <640): features
   - `hr.border-t.border-latte-125.mb-4` (1px #c7c3c0 top border, mb 16).
   - `ul.space-y-2.5.sm:space-y-3`: li `flex items-start gap-2.5 sm:gap-3` (gap **12** ≥640 / **10** <640; vertical spacing **12** ≥640 / **10** <640 as margin-bottom on each li except the last). li height 22 (check) / 23 (cross).
     - Icon svg `mt-0.5 flex-shrink-0` (mt 2): check `plan-check.svg` **20x20** fill **#008A56**, or cross `plan-x.svg` **20x21** fill and stroke **#ED614B** (stroke-width .125).
     - span label.
   - `hr.border-t.border-latte-125.mt-4` (mt 16).
3. `div.mb-6` (mb 24): price block.

Content:

**Card 1: Riley Plus+**
- h3 "Riley Plus+"
- p "For families who parent as a team" + 3 avatars: purple1.svg, purple2.svg, purple3.svg (gap 2)
- tagline (green) "Try it free for 7 days"
- features (all check, #008A56): Unlimited Children & Tracking; 3+ Caregivers with their own logins; Unlimited Chats; Tracking Insights; Seamless Sharing; Advanced Memory & Customization
- price block: p "Starting at" (mb 8); div "$9.99 " + span "/ month"; p "Billed monthly, quarterly or annually"; p green "Your first 7 days are free"

**Card 2: Riley Basic**
- h3 "Riley Basic"
- p "For solo parenting or simpler setups" + 1 avatar purple1.svg
- tagline (green) "Always free"
- features: Unlimited Children & Tracking (**check**); then **cross (#ED614B)** for: 3+ Caregivers with their own logins; Unlimited Chats; Tracking Insights; Seamless Sharing; Advanced Memory & Customization
- price block: div "Free" (Recoleta 32/48, mb 8); p `flex items-center gap-2` "Available on:" + Apple glyph svg **16x16** (`w-4 h-4 text-text-primary`, `fill=currentColor` → #2e2a42, viewBox 0 0 24 24) = `public/assets/pages/pricing/apple-small.svg`. As an `<img>` its currentColor would render black, so inline it or set the fill to #2e2a42.

### 3.6 CTA
- Wrapper `div.text-center.px-4.sm:px-0`. Shared `Button` (§0.6 of the homepage spec) with the extra classes listed in §1.4. Measured padding 16px 32px, radius 32, gap 14, bg #5934c5 inline, white text. The inner span (padding 0 20, gap 8) holds "Get Started For Free" plus `button-arrow.svg` (16x17, `fill=currentColor` → white; inline it or set the fill to #fff).
- Click destination: the browser ended on **https://apps.apple.com/us/app/riley-child-development-coach/id6738063220**. It is JS navigation and not in the DOM. Whether it passes through a onelink redirect is **UNVERIFIED** (no onelink request was captured). Using the homepage's `https://rileyapp.onelink.me/JNxh/nativeappstorebutton` is a reasonable equivalent.
- Hover / active: same JS inline colours as every `Button`.

### 3.7 Motion
- No load or scroll-reveal animation on the content: computed opacity, transform and inline styles of the first 40 content nodes were identical at load and 2.5s later, and there are no framer inline styles.
- Clouds: horizontal float keyframes (M3: floatSlow 100s / floatMedium 85s / floatFast 50s linear infinite, `.cloud-alt` delays -50s / -42.5s / -15s) plus scroll parallax (M3b) exactly as on the homepage. The progress formula is in §1.4.
- CTA hover per M10. Cards have no hover.

### 3.8 Assets used by PricingHero
| File | Status | Rendered |
|---|---|---|
| `/assets/icons/hero-cloud-1..4.svg` | already present (identical) | 411x251 / 592x362 / 411x251 / 473.6x289.6 (scaled) |
| `/assets/purple1.svg`, `purple2.svg`, `purple3.svg` | already present. Original path `/mascots/avatars/purpleN.svg` was downloaded and is **byte-identical**, so no new file | 24x24 (20x20 <640) |
| `/assets/pages/pricing/plan-check.svg` | NEW (extracted from inline SVG) | 20x20, #008A56 |
| `/assets/pages/pricing/plan-x.svg` | NEW (extracted from inline SVG) | 20x21, #ED614B |
| `/assets/pages/pricing/apple-small.svg` | NEW (extracted from inline SVG, currentColor) | 16x16 |
| `/assets/pages/pricing/button-arrow.svg` | NEW (extracted from inline SVG, currentColor) | 16x17 |

### 3.9 New tokens to add to tailwind.config.js (if not present)
- `latte-125`: **#c7c3c0** (card border, hr)
- `sea-green-100`: **#4ca67e** (green taglines)
- `bg-pricing-radial`: `radial-gradient(45.01% 50.02% at 50% 52.71%, #ff914d 0, #f9f5f1 100%)`
- Muted text: `text-text-primary/70` = rgba(46,42,66,.7)

---

## 4. Page-level summary

### 4.1 Document height (px)
| Route | 1440 | 1280 | 768 | 390 |
|---|---|---|---|---|
| /pricing | **5643** | 5789 | 5098 | **6154** |
| 8 landing slugs (404 template) | **1478** | 1478 | 1166 | **1293** |

### 4.2 /pricing section heights (px)
| Section | 1440 | 1280 | 768 | 390 |
|---|---|---|---|---|
| AnnouncementBar | 54.4 | 54.4 | 0 | 0 |
| SiteHeader | 80 | 80 | 80 | 80 |
| PricingHero | 1099.3 | 1099.3 | 1043.3 | 1471.8 |
| Testimonials | 1058 | 1125.6 | 816 | 1076.6 |
| GradientBand (table only) | 1250.2 | 1250.2 | 1065.4 | 1176.6 |
| FaqClouds | 900 | 900 | 1100 | 1100 |
| FinalCta | 708 | 786 | 440 | 536 |
| SiteFooter | 493.6 | 493.6 | 553.6 | 713.4 |

### 4.3 404-template section heights (px)
| Section | 1440 | 1280 | 768 | 390 |
|---|---|---|---|---|
| AnnouncementBar | 54.4 | 54.4 | 0 | 0 |
| SiteHeader | 80 | 80 | 80 | 80 |
| NotFoundPage | 850 | 850 | 532.5 | 500 |
| SiteFooter | 493.6 | 493.6 | 553.6 | 713.4 |

### 4.4 Title / meta
| Route | `<title>` | meta description | robots | canonical |
|---|---|---|---|---|
| /pricing | Riley – Baby Tracker & Child Development Expert | "Riley learns and grows with your family, offering personalized, data-backed guidance so you're ready for anything life—or your kids—throw your way." | index, follow | `https://www.rileyapp.com/` (points at the homepage, a live quirk) |
| all 8 landing slugs | same title | same description | **noindex** | UNVERIFIED |

---

## 5. Assets downloaded for these pages
| Local path | Original | Notes |
|---|---|---|
| `public/assets/shared/background.bc1c0c29.svg` | `https://rileyapp.com/_next/static/media/background.bc1c0c29.svg` (served via `_next/image?...&w=1920` / `w=3840`) | 404 illustration, 1440x561 |
| `public/assets/pages/pricing/plan-check.svg` | inline SVG in PricingHero | |
| `public/assets/pages/pricing/plan-x.svg` | inline SVG in PricingHero | |
| `public/assets/pages/pricing/apple-small.svg` | inline SVG in PricingHero | currentColor |
| `public/assets/pages/pricing/button-arrow.svg` | inline SVG in PricingHero CTA | currentColor |

Every other image on /pricing (wordmark, testimonial purple1–5, FAQ portraits 2–6.png, riley-up.svg, background-clouds(1).svg, mascots.svg, table check icons, footer icons) is already in `public/assets/`. No video, .riv or new fonts are loaded on either template.

---

## 6. Gaps / UNVERIFIED
- The 8 sitemap landing routes have **no content** live or in the Wayback Machine. Their intended landing-page designs cannot be measured. Only the shared 404 template is specced.
- The PricingHero CTA's intermediate redirect (onelink or direct App Store) is not exposed in the DOM. Only the final App Store URL was observed.
- The 404 `<img>` alt text and the 404 pages' canonical tag were not captured.
- The live 404 header wordmark fails to load (live bug). Its rendered state is assumed to match the homepage header.
- 1280 and 768 /pricing values came from resizing after load (the 1280 navigation aborted once and was retried). Layout is fully responsive, so measurements should be equivalent to a fresh load.
