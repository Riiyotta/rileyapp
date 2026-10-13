Source: https://rileyapp.com/

# Riley homepage: clone spec

Recon date: 2026-10-13. Measured live with Playwright (Chromium) at 1440x900, 1280x800, 768x1024 and 390x844, and cross-checked against the saved Next.js build ("Riley – Baby Tracker & Child Development Expert.html" + `_files/*.css|*.js`). Values are computed styles or getBoundingClientRect results unless marked **UNVERIFIED**. Asset files are listed in `ASSET_MANIFEST.md`.

The original is built with Next.js, **Tailwind v4** (custom theme), framer-motion, embla-carousel-react, react-scroll-parallax (ParallaxBanner), @rive-app/react (webgl2 2.30.4) and Storyblok CMS content.

---

## 0. Global / page-level

### 0.1 Page
| | 1440 | 1280 | 768 | 390 |
|---|---|---|---|---|
| Total document height | **11464px** | 11756px | 14253px | 14351px |
| Announcement bar | visible (54.4px) | visible | hidden (`hidden lg:flex`) | hidden |

- `body` background **#f9f5f1** (`--background`, "Primary-Latte"). Default text color `oklch(14.5% 0 0)` = **#0a0a0a**. Default body font: `sansRegular` (Cadiz Regular) 16px/24px.
- `html` has `font-sans` and all font variable classes.
- The widest content wrapper is `max-w-[90rem]` = **1440px**. The hero content uses `max-w-[80rem]` = 1280px. Side padding varies by section and is given per section below. There is no single global container.
- No horizontal scroll on the page. Sections with clouds/marquees use `overflow:hidden`.

### 0.2 Breakpoints (Tailwind v4 theme on the original)
`sm` 40rem = **640px**, `md` 48rem = **768px**, `lg` 62rem = **992px**, `xl` 80rem = **1280px**, `2xl` 90rem = **1440px**. `max-md:` = <768px. Extra raw media queries: `(max-width:960px)` / `(min-width:961px)` in the FAQ and comparison-table modules, `(max-width:639px)` (JS matchMedia, blog carousel), `(min-width:1024px)` / `(max-width:767px)` for `.embla__slide`.

For Tailwind v3, use `screens: { sm:'640px', md:'768px', lg:'992px', xl:'1280px', '2xl':'1440px' }`.

### 0.3 Color tokens (measured hex)
| Token (original class) | Hex | Usage |
|---|---|---|
| text-text-primary | **#2e2a42** | almost all headings and body copy |
| purple-100 / button "dark-purple" base | **#5934c5** | primary buttons, nav links, footer links, icons |
| button hover | **#7a55fd** | primary button hover (JS inline style) |
| button active (mousedown) | **#5a20e1** | |
| violet-100 (lilac) | **#d7befc** | announcement bar, press strip, superpower card, testimonial card, feature card 2 |
| latte-150 / body | **#f9f5f1** | page bg, testimonials section bg, comparison-table panel |
| latte-100 | **#fcfbfa** | "How Riley Works" section bg |
| orange-100 (tangerine) | **#ff914d** | featurette card bg |
| orange-70 (apricot) | **#ffa552** | feature card 1 |
| yellow-100 (marigold) | **#ffd55d** | feature card 3 |
| orange-200 | #ffd6a7 | "Development" blog pill |
| slate-100 | #f1f5f9 | "Feeding"/"News"/"Pregnancy" pills |
| red-200 | #ffc9c9 | "Health" pill |
| stone-200 | #e7e5e4 | "Sleep" pill |
| slate-800 | **#1d293d** | section-2 paragraph, clinical names, pill text |
| gray-300 | #d1d5dc | header nav divider |
| gray-700 (prose body) | #364153 | announcement text, prose paragraphs |
| gray-900 (prose bold) | #101828 | announcement link, prose `<strong>` |
| gray-50 | #f9fafb | superpower card hover bg |
| white | #ffffff | cards |
| star yellow | #ffdd7d | testimonial stars |

Gradients:
- Features/comparison wrapper: `radial-gradient(534.59% 131.83% at 43.09% 3.04%, #FF93AB 0%, #FF9C7F 2.14%, #FFA168 23.66%, #F9F5F1 65.12%)`
- FAQ section: `radial-gradient(rgb(165,201,242) 0, #f9f5f1 70%) no-repeat; background-size:200% 100%; background-position:50%`
- Superpower modal: per mascot (see §4.2).

Shadows:
- `shadow` / `shadow-sm`: `0 1px 3px 0 #0000001a, 0 1px 2px -1px #0000001a`
- `shadow-md`: `0 4px 6px -1px #0000001a, 0 2px 4px -2px #0000001a`
- `shadow-2xl` (modal): `0 25px 50px -12px #00000040`

Radii: 24px (`rounded-3xl`) on cards/sections, 30px featurette card, 35px blog image, 32px buttons (`rounded-[2rem]`), 40px blog pills, 16px table panel/cells, 9999px avatars/round buttons.

### 0.4 Fonts / @font-face
The families are **Cadiz** (sans) and **Recoleta Regular** (serif). The real names were read from the WOFF2 `name` tables. Files are in `public/fonts/`. The original registers each cut as its own family with Next.js size-adjusted Arial fallbacks:

```css
@font-face{font-family:sansRegular;src:url(/fonts/Cadiz-Regular.woff2) format("woff2");font-display:swap;font-weight:400}
@font-face{font-family:sansRegularItalic;src:url(/fonts/Cadiz-RegularItalic.woff2) format("woff2");font-display:swap;font-weight:400}
@font-face{font-family:sansBook;src:url(/fonts/Cadiz-Book.woff2) format("woff2");font-display:swap;font-weight:350}
@font-face{font-family:sansBookItalic;src:url(/fonts/Cadiz-BookItalic.woff2) format("woff2");font-display:swap;font-weight:350}
@font-face{font-family:sansSemibold;src:url(/fonts/Cadiz-SemiBold.woff2) format("woff2");font-display:swap;font-weight:600}
@font-face{font-family:sansSemiboldItalic;src:url(/fonts/Cadiz-SemiBoldItalic.woff2) format("woff2");font-display:swap;font-weight:600}
@font-face{font-family:sansBold;src:url(/fonts/Cadiz-Bold.woff2) format("woff2");font-display:swap;font-weight:700}
@font-face{font-family:sansBoldItalic;src:url(/fonts/Cadiz-BoldItalic.woff2) format("woff2");font-display:swap;font-weight:700}
@font-face{font-family:sansBlack;src:url(/fonts/Cadiz-Black.woff2) format("woff2");font-display:swap;font-weight:800}
@font-face{font-family:sansBlackItalic;src:url(/fonts/Cadiz-BlackItalic.woff2) format("woff2");font-display:swap;font-weight:800}
@font-face{font-family:"serif";src:url(/fonts/Recoleta-Regular.woff2) format("woff2");font-display:swap;font-weight:400}
/* Next.js metric-matched fallbacks */
@font-face{font-family:"sansRegular Fallback";src:local("Arial");ascent-override:92.53%;descent-override:23.50%;line-gap-override:19.34%;size-adjust:103.42%}
@font-face{font-family:"sansBold Fallback";src:local("Arial");ascent-override:91.58%;descent-override:23.25%;line-gap-override:19.14%;size-adjust:104.49%}
@font-face{font-family:"sansSemibold Fallback";src:local("Arial");ascent-override:91.94%;descent-override:23.34%;line-gap-override:19.21%;size-adjust:104.09%}
@font-face{font-family:"sansBook Fallback";src:local("Arial");ascent-override:92.87%;descent-override:23.58%;line-gap-override:19.41%;size-adjust:103.05%}
@font-face{font-family:"serif Fallback";src:local("Arial");ascent-override:100.82%;descent-override:36.29%;line-gap-override:0.00%;size-adjust:99.19%}
```
No `unicode-range` is declared.

Font stacks: `font-sans` / `font-sans-regular` = `sansRegular,"sansRegular Fallback"`; `font-sans-bold` = `sansBold,"sansBold Fallback"`; `font-sans-semibold` = `sansSemibold,"sansSemibold Fallback"`; `font-serif` = `"serif","serif Fallback"` (with `ui-serif` appended in one utility).

**Weight quirk:** `font-sans-bold` / `font-sans-semibold` only swap the family, so the computed `font-weight` stays **400** while the bold or semibold face renders. `<strong>` and `font-bold` inside `sansRegular` text compute to 700/600 against a family that only has a 400 face, so Chrome draws **synthetic bold**. Keep these exact families and weights to match the rendering.

**Unlayered type rules on the original:** these sit outside `@layer`, so they beat utilities. Apply them the same way:
```css
h1{font-family:var(--font-serif)}
@media (max-width:62rem){h1{font-size:2.5rem;line-height:3rem}}
@media (min-width:62rem){h1{font-size:4rem;line-height:4.5rem}}
@media (min-width:62rem){.desktop-h1{font-size:5rem;line-height:6rem;font-family:serif}
  .desktop-h2{font-size:3.75rem;line-height:4.875rem;font-family:serif}
  .desktop-h3{font-size:2.5rem;line-height:3rem;font-family:serif}
  .desktop-h4{font-size:1.625rem;line-height:2.1125rem;font-family:serif}
  .desktop-body{font-size:1.25rem;line-height:1.875rem;font-family:sansRegular}}
@media (max-width:62rem){.mobile-h1{font-size:2.5rem;line-height:3rem;font-family:serif}
  .mobile-h2{font-size:1.625rem;line-height:2.1125rem;font-family:serif}
  .mobile-h3{font-size:1.25rem;line-height:2.1125rem;font-family:serif}
  .mobile-h4{font-size:1rem;line-height:1.3rem;font-family:serif}
  .mobile-body{font-size:1rem;line-height:1.5rem;font-family:sansRegular}}
```
The `lg:desktop-*` utility variants sit in the utilities layer and set only size and line-height: `lg:desktop-h4` = 24px/33.8px, `lg:desktop-h3` = 40px/48px, `lg:desktop-h2` = 60px/78px, `lg:desktop-body` = 20px/30px. They do **not** set the family. That is why `lg:desktop-h4` headings render in Cadiz at ≥992px while `mobile-h3` headings switch to Recoleta below 992px. The per-section tables below give the resulting computed values.

### 0.5 Typography roles (computed)
| Role | ≥992 (1440/1280) | <992 (768/390) |
|---|---|---|
| Hero H1 | Recoleta 64px/72px, ls normal, #2e2a42 | Recoleta 40px/48px, centered |
| Section H2 (`desktop-h3`/`lg:desktop-h3`) | Recoleta 40px/48px | Recoleta 26px/33.8px |
| Big H2 ("How Riley Works", final CTA) | Recoleta 60px/78px | Recoleta 40px/48px |
| FAQ H2 | Recoleta 80px/104px, **#0a0a0a** | Cadiz Regular 40px/52px (≤960) |
| Eyebrow / sub-heading (`lg:desktop-body`) | Cadiz Regular 20px/30px | Cadiz Regular 16px/24px |
| Body large | Cadiz Regular 20px/30px | 16px/24px |
| Body | Cadiz Regular 16px/24px | same |
| Card title (`lg:desktop-h4`) | Cadiz Regular 24px/33.8px | Recoleta 20px/33.8px (`mobile-h3`) |
| Superpower card label | Recoleta 24px/33.8px | Recoleta 16px/20.8px |
| Testimonial quote | Recoleta 26px/33.8px | Cadiz Regular 24px/33.8px |
| Nav link | Cadiz Bold face (fw 400 computed) 18px/24px, #5934c5 | n/a |
| Button | Cadiz Bold face 16px/24px, #fff | same |
| Blog card title | Recoleta 20px/26px, underline | Recoleta 14px/18.2px |
| Blog pill | Cadiz Bold 14px/20px, fw 700, #1d293d | same |
| Footer link | Cadiz SemiBold face 16px/24px, #5934c5 | same |
| Caption (© line) | Cadiz Regular 14px/19.6px | same |
| Letter-spacing | `normal` everywhere except the announcement bar (-0.16px) | |

### 0.6 Primary button component (`Button`, used for every purple CTA)
- `<button class="button-primary font-sans-bold inline-flex w-full items-center justify-center gap-3.5 whitespace-nowrap rounded-[2rem] px-8 py-4 transition-all duration-300 cursor-pointer">` with inner `<span class="flex max-w-full items-center justify-center gap-2 px-5">TEXT</span>`.
- Computed: padding 16px 32px (plus inner span padding 0 20px), radius 32px, gap 14px, height **56px**, Cadiz Bold face 16px/24px, white text, nowrap. Width comes from the parent wrapper `max-w-[14rem]` (224px) or text width.
- Colors are set by JS as **inline style**: base `background-color:#5934C5; color:#FFF`; on `mouseenter` **#7A55FD**; on `mousedown` **#5A20E1**; reset on `mouseleave`/`mouseup`. Transition `all 300ms cubic-bezier(0.4,0,0.2,1)`. Disabled state: bg `rgb(208,183,243)`, color #000, opacity .4, cursor not-allowed.
- Button widths at 1440: "Get Started For Free" 224px (in max-w-[14rem] wrapper; header one is 251.3px), "Talk to Riley" 224, "Join the club" 197.7, "Join Riley—early, easy, free" 240 (max-w-[15rem]), "Explore the blog" 223.7, "Get support that gets you" 289.1 (max-w-[20rem]), FAQ "Learn More" 187.4x60 (line-height 28px inherited from prose).
- Link targets: the header CTA, "Try For $0" and mobile menu CTA go to `https://rileyapp.onelink.me/JNxh/nativeappstorebutton`; "Get support that gets you" also uses this onelink in the Storyblok payload; FAQ "Learn More" goes to `/pricing`. Other CTA targets are **UNVERIFIED**. They navigate via JS router and are not exposed in the DOM.

### 0.7 Suggested component tree
`AnnouncementBar` → `Hero` (contains `SiteHeader`, `HeroParallaxClouds`, `HeroContent`, `PressMarquee`) → `PersonalizationMarquee` → `Superpowers` (+ `SuperpowerModal`) → `Featurette` (`RiveChatSlide`) → `ClinicalBoard` → `HowRileyWorks` → `Testimonials` → `GradientBand` (`FeatureCards`, `ComparisonTable`) → `FaqClouds` → `BlogTeaser` → `FinalCta` → `SiteFooter`. Shared: `Button`, `Marquee`, `RoundArrowButton`, `CloudSvg`.

---

## 1. AnnouncementBar (y 0, h 54.4 @1440)
- `<div><aside class="hidden lg:flex w-full items-center justify-center px-0 py-3 text-center">`, inline `background-color: rgb(215,190,252)` (**#d7befc**), padding 12px 0. Hidden below 992px.
- Text (inside `.prose`, p margins 0): `<p>` → `<a href="https://rileyapp.com/pricing">Try Riley risk free with our 7-day free trial!</a>`.
  - p: Cadiz Regular 16px / **30.4px** (leading-[1.9rem]), letter-spacing **-0.16px**, color #364153.
  - a: font-weight 500, underline, color #101828. Block width 294.4px, centered.

---

## 2. Hero (wrapper `div.relative.w-full.overflow-hidden`; y 54, h 909.9 @1440 and @1280; h 1483.2 @768, h 1449.9 @390)

### 2.1 Structure
```
div.relative.w-full.overflow-hidden
├─ div.absolute.inset-0.w-full            ← ParallaxBanner (4 cloud layers, see 2.6)
└─ header.relative.mx-auto.w-full
   ├─ SiteHeader (motion.header)          h 80
   ├─ HeroContent                         h 685.9 @1440
   └─ PressMarquee wrapper                h 144 (80 strip + 64 pb)
```

### 2.2 SiteHeader
- `header`: flex items-center, padding 12px 16px; `md:` padding-x **60px**. Height 80px. Initial state `relative z-[100] bg-transparent`.
- Inner: `flex w-full items-center justify-between md:mx-auto md:max-w-[90rem]` (max 1440), height 56.
- Logo: `a.relative.h-[52px].w-[90px]` → img `wordmark.svg` rendered **79x52** at x 60. Links to `/`.
- Desktop nav (`hidden lg:flex flex-1 items-center justify-between lg:pl-12`, padding-left 48px):
  - Left group `flex flex-1 items-center justify-end gap-12` (gap 48px): "Blog" (link `https://rileyapp.com/blog`) and "What's New?" (button that opens a changelog modal, out of scope). Both Cadiz Bold face 18px/24px, #5934c5, `hover:opacity-80` with 150ms ease-in-out cubic-bezier(.4,0,.2,1). At 1440: Blog x 871, w 38.1; What's New? x 957, w 106.9.
  - Divider `span.mx-8.h-6.w-px.bg-gray-300`: 1x24, #d1d5dc, margin 0 32px.
  - CTA Button "Get Started For Free" (`data-button-id="header-nav-cta"`), **251.3x56** at x 1129.
- Mobile (<992): the nav is hidden. Right side shows `div.flex.gap-5` (gap 20):
  - Button "Try For $0" (class adds `max-w-[100px] px-3 py-2`). Measured **100x56**.
  - Hamburger `button.relative.z-[1003].text-2xl` 28x56 holding `menu-hamburger.svg` (28x23, stroke #2E2A42 1.975, round caps). When open it swaps to `menu-close.svg` (23x24).
  - At 390 the header padding is 12px 16px and the logo sits at x 16.
- Sticky behavior: see §14 Motion M2.

### 2.3 Mobile menu (<992; measured at 768)
- Opening sets `document.body.style.overflow = hidden`. Header classes become `relative bg-beige-100/60 z-[1002] backdrop-blur-xl`. `bg-beige-100` is not defined in the CSS, so the computed bg stays transparent and only `backdrop-filter: blur(24px)` applies.
- Portal into `<body>` (framer-motion AnimatePresence):
  1. Backdrop `div.fixed.inset-0.backdrop-blur-sm`, z-index 1000, blur(8px), bg transparent (the beige class is undefined). Click closes.
  2. Panel `motion.div.fixed.inset-0.backdrop-blur-xl`, z 1001, blur(24px). Animation: `initial {y:'100%'} → animate {y:0}`, exit `{y:'100%'}`, `duration .25`.
  3. Content `div.flex.h-full.flex-col.px-5.pt-24.pb-[3.75rem]` (padding 96px 20px 60px), color #2e2a42:
     - `div.flex.w-full.flex-col.items-center.gap-8` (gap 32): items Cadiz SemiBold face 20px/28px centered: "Blog" (an expander: clicking toggles sub-links "All" + blog categories fetched from `/api/get-blog-categories`, each `motion.div` with `initial {opacity:0,y:-10} → {opacity:1,y:0}`; the sub-link list is **UNVERIFIED**, the API returned nothing to the test session) and "What's New?". Both `hover:opacity-80`.
     - Bottom `div.mt-auto.w-full.p-4.text-center` holding Button "Get Started For Free" `w-full max-w-xs` (320x56).

### 2.4 HeroContent
- `div.relative.z-50.mx-auto.flex.w-full.max-w-[80rem].flex-col.items-center.px-8.py-8.pb-[10rem] max-md:gap-12 lg:flex-row lg:py-[5rem]`.
  - @1440: x 80, w 1280, padding **80px 32px**, h 685.9. @1280: x 0 (same padding). @768: column, padding 32px 32px 160px. @390: column, gap 48.
- **Left column** `flex flex-1 flex-col items-center gap-10 max-md:gap-6 max-md:px-4 lg:order-1 lg:items-start xl:min-w-[45rem]`: @1440 720x476 at (112, 239), gap 40. @390 gap 24, padding-x 16.
  - Title group `relative flex flex-col items-center gap-6 max-md:gap-4 lg:min-w-[33.5rem] lg:items-start` (gap 24; 16 on mobile).
    - Inner `relative mx-0 flex flex-col items-center justify-center gap-6 lg:inline-flex lg:items-start lg:gap-0`.
      - Mobile-only mascot: `img.flex.w-[5.8rem].lg:hidden` → HeroRiley.svg **92.8x101.2**, centered above the H1 (<992).
      - **H1** (`text-[clamp(2.5rem,6vw,5rem)] leading-none`; the unlayered h1 rule wins): Recoleta **64px/72px** left-aligned ≥992; **40px/48px** centered <992. Color #2e2a42. Box 720x166 @1440.
        Markup: `<span class="block">Panic Scrolling Stops Here. Meet <span class="inline-flex items-baseline gap-3"><img class="ml-3 hidden w-[4.5rem] translate-y-[0.25em] lg:inline-block" src=HeroRiley.svg> <span>Riley.</span></span></span>`.
        Measured line breaks @1440 (720px box): line 1 "Panic Scrolling Stops" (x 112), line 2 "Here. Meet [mascot img 72x78.5 at x 430.6, ml 12, translateY .25em] Riley." Inline span gap 12.
    - Paragraph `mobile-body lg:desktop-body max-w-[31.25rem] text-center lg:text-left` (max-w 500): Cadiz Regular **20px/30px** (16/24 below 992), #2e2a42, 500x150 @1440 (5 lines). Text:
      "Get instant, pediatrician-backed parenting support the moment you need it. Riley has **award-winning, 24/7 advice tailored to your family** with smart tracking and guidance. Parent confidently, with **the only parenting app you'll ever need.**" Bold parts are `span.font-sans-bold` (Cadiz Bold face).
  - CTA group `mx-0 mb-28 flex w-full flex-col items-center justify-center gap-4 self-stretch lg:mb-0 lg:items-start` (gap 16; mb 112 below lg):
    - Button "Get Started For Free" `max-w-[14rem]` → 224x56.
    - `div.flex.items-center.justify-center.gap-2.5` (gap 10): `p` "Available on:" Cadiz Regular 16px/24px #2e2a42 (93.7 wide) + `apple-logo.svg` 14x16.
- **Right column** `relative -z-15 -mt-12 md:-mt-8 flex justify-center overflow-visible lg:order-2`: @1440 640x557.9 at (832, 182), margin-top -32 (md+), -48 below md.
  - img `HeroIllo.84fc0736.svg` class `mx-0 max-w-[25rem] scale-250 self-center md:max-w-[40rem] lg:translate-x-[-4rem] lg:scale-200`.
    - Layout box: ≥768 max-w 640 (640x557.9); <768 max-w 400.
    - Visual: `scale: 2` + `translate: -4rem` at ≥992 (visual 1280x1116 at x 448, y -97); `scale: 2.5` below 992 (1600 wide at 768, 1000 wide at 390). Visually the illustration fills most of the hero behind the text, and the hero wrapper clips it.
  - <992 the image column renders below the text (order) at y 797 @390.

### 2.5 PressMarquee
- Wrapper `div.flex.w-full.pb-16` (padding-bottom 64). Strip `div.relative.flex.w-full.flex-col.items-center.justify-center.overflow-hidden.bg-violet-100`: **1440x80**, bg #d7befc.
- Mask on inner `div.w-full`: `mask: linear-gradient(90deg, transparent, black 20%, black 80%, transparent)`.
- Marquee: `div.group.flex.overflow-hidden.p-2 [--gap:1rem] [gap:var(--gap)] flex-row [--duration:20s]` (padding 8, gap 16). It contains **4 identical copies** of the row `div.flex.shrink-0.justify-around.[gap:var(--gap)].animate-marquee` (1232x64 each).
- Row items (order: NBC, Axios, Bump, Finsmes, TC, Glamour): `div.mx-8.flex.h-16.w-32.items-center.justify-center` (128x64, margin 0 32px) → `img.h-auto.max-h-6.w-full.object-contain` (128 wide, max-h 24; Finsmes renders 128x12.9, TC 128x21.5). Files: nbc.png, axios.png, bump-logo.png, finsmes.png, tc.png, glamour.png. Alt "NBC logo", "Axios logo", and so on.
- Animation: §14 M4.

### 2.6 Hero parallax clouds (ParallaxBanner background)
`div.lg:h-120vh.absolute.inset-0.w-full` (the `h-120vh` class is not defined in CSS; the box equals the hero wrapper). It holds 4 stacked layers, each `div.absolute.inset-0` → `div.h-full.w-full(.bg-transparent).relative.overflow-hidden` → a layer div with inline `position:absolute; inset:<top> 0 0; will-change:transform; transform:translateY(x%)`. Layer z-index: layer 1 (no z, wrapper `.bg-hero`), layer 2 `-z-50`, layer 3 `-z-30`, layer 4 `-z-10`. All are `pointer-events-none`.

| Layer | translateY range | Extra | Inset top (expanded) | Clouds (each wrapper `.cloud-wrapper` = absolute, pointer-events none, will-change transform, transform-origin center) |
|---|---|---|---|---|
| 1 | 0 → **-20%** | | -(20% of banner height), e.g. -181.99px @1280 | 2× `hero-cloud-1.svg` 411x251, wrapper `-right-40 top-10` (right -160px, top 40px), `animate-float-slow` (+ `.cloud-alt`) |
| 2 | 0 → **-35%** | | -(35% of banner h) | 2× `hero-cloud-2.svg` 592x362 `-left-30 top-30` (left -120, top 120), float-medium; 2× `hero-cloud-3.svg` 411x251 `top-1/2` (top 50%, left 0 computed), float-medium |
| 3 | 0 → **-50%** | | -(50% of banner h) | 2× `hero-cloud-1.svg` `-left-30 bottom-20` (left -120, bottom 80), float-fast; 2× `hero-cloud-3.svg` `-right-40` (top 0), float-fast |
| 4 | 0 → **-100%** | `scale .8 → 1.2`, not expanded (inset 0) | 0 | inner `div.absolute.inset-0` with inline `transform:translateY(25%)`; 2× `hero-cloud-4.svg` (vb 592x362, width/height attrs, rendered **473.6x289.6** under the 0.8 scale), wrappers `-left-20` (left -80) / `left-20` (left 80), float-fast |

Each layer's horizontal motion comes from the cloud keyframes (§14 M3). The horizontal start offsets are effectively the animation delays.

---

## 3. PersonalizationMarquee (y 964, h 664 @1440)
- `section.flex.flex-col.items-center.self-stretch.pb-12.lg:pb-0` (padding-bottom 48 below 992).
- Inner `div.flex.w-full.flex-col.items-center.gap-8.overflow-hidden lg:gap-12 lg:py-20`: gap **48**, padding **80px 0** (≥992). Below 992: gap 32, no vertical padding.
- H2 `desktop-h3 ... px-12 text-center lg:px-0`: "Parenting isn't one-size-fits-all.`<br>`Your support shouldn't be, either." Recoleta 40px/48px ≥992, 1440x96 full width. Below 992: **Cadiz Regular 40px/48px** (the utility-layer `desktop-h3` size stays; the serif family only applies ≥992), padding 0 48px; 768x96 @768, 390x240 (5 lines) @390.
- Marquee (1440x184): same Marquee component, `p-2 [--gap:1rem] flex-row gap-[3rem] [--duration:50s]` (computed container gap **48px**; the rows use `gap:var(--gap)` = 16px), rows `animate-marquee [animation-direction:reverse]`, 4 copies, **no mask**.
  - Items `div.flex.h-[10.5rem].w-auto.items-center.justify-center` (168 tall) → `img.h-[10.25rem].w-full.object-contain` (164 tall). Order and widths: softie-family 142, spark-family 208.7, uplifter-family 250.5, riley-family 208.7, worrier-family 180.1, guide-family 224. Alts "Softie logo", "Spark logo", "Uplifter logo", "Riley logo", "Worrier logo", "Guide logo". Row width 1294.
- H4 `px-12 text-center text-xl leading-8 text-slate-800 lg:w-[458px] lg:px-0`: 458x128 @1440, Cadiz Regular **20px/32px**, **#1d293d**. Text: "Riley learns and remembers what matters: your baby's growth stage, tracking logs, and past wins to give guidance that fits your family.`<br>`" + `span.font-sans-bold.mt-8.lg:mt-0` "Support that thinks, adapts, and grows with you."

---

## 4. Superpowers (`section` y 1628 @1440, h 664; h 746.8 @1280, 931.6 @768, 947.8 @390)

### 4.1 Layout
- `section.text-text-primary.relative.mx-auto.flex.w-full.max-w-[90rem].flex-col.items-center.justify-center.px-4.py-4 max-md:px-5 lg:px-11 2xl:px-4`. Padding: 16px @1440, **16px 44px** @1280, 16px @768, 16px 20px @390.
- Inner card `div.flex.w-full.flex-col.items-center.rounded-3xl.bg-violet-100`:
  - @1440: 1408x632, **padding 80px 224px 120px**, gap **48**, radius 24, bg #d7befc.
  - @768: padding 60px 16px 120px, gap 40. @390: padding 60px 20px 96px.
- H2 `mobile-h2 lg:desktop-h3 max-w-[33.5rem] text-center font-serif`: "What Parenting Superpower Do You Need Today?" Recoleta 40px/48px (26/33.8 <992), 536x96 (2 lines).
- Grid `div.grid.w-full.gap-9.lg:grid-cols-2`: gap **36px**. Columns 462px+462px @1440 (grid 960 wide), 354+354 @1280, 1 column below 992 (704 @768, 310 @390).
- Card `article[role=button][tabindex=0].flex.w-full.items-center.justify-between.gap-10.rounded-3xl.bg-white.px-5.py-4.shadow.transition.hover:bg-gray-50`:
  - 462x72 @1440 (99.6 tall @1280 because the labels wrap to 2 lines), padding **16px 20px**, gap 40, radius 24, `shadow` (0 1px 3px 0 #0000001a, 0 1px 2px -1px #0000001a), hover bg **#f9fafb**, transition color/bg/etc. 150ms cubic-bezier(.4,0,.2,1).
  - Left `div.flex.items-center.gap-5` (gap 20): icon img 40x40 `object-contain`, then label `span.lg:desktop-h4.mobile-h4.font-serif`: Recoleta **24px/33.8px** (16px/20.8px <992), #2e2a42.
  - Right: `card-arrow.svg` 13x12.
  - Items (icon → label): bottle.svg "Survive the newborn stage"; moon.svg "Get help with naps and sleep"; blocks.svg "Support baby development"; stubborn.svg "Navigating toddler tantrums"; bowl.svg "Starting solid foods"; sailboat.svg "Build a routine".
  - Click or Enter/Space opens the SuperpowerModal.
- Decorative mascot: `img.absolute.-bottom-20.left-12` = **mascot.svg 177x179**, left 48px, bottom -80px. It overhangs 80px into the next section and is not clipped.

### 4.2 SuperpowerModal (portal into `<body>`, no entry animation)
- Overlay `div.fixed.inset-0.z-40.bg-black/40` (rgba(0,0,0,.4)). Click closes.
- Scroller `div.fixed.inset-x-0.bottom-0.z-150.flex.max-h-[100dvh].items-start.justify-center.overflow-y-auto.rounded-3xl.p-4.pb-0.shadow-2xl lg:inset-0 lg:items-center` (padding 16 16 0).
- Dialog `section[role=dialog].relative.flex.w-full.max-w-[32rem].flex-col.gap-4.rounded-3xl.shadow-2xl lg:max-w-[90vw] lg:gap-12 lg:px-25`. @1440: 1296x707 at (72, 104), padding 0 100px, gap 48, radius 24, shadow `0 25px 50px -12px #00000040`. Background per mascot:
  - worrier `radial-gradient(58.33% 52.53% at 50% 50%, #D7BEFC 0%, #FFF 100%)`; guide `radial-gradient(64.92% 39.36% at 50.04% 52.53%, #4598E6 0%, #FFF 100%)`; softie `radial-gradient(64.92% 39.36% at 50.04% 52.53%, #62D09E 0%, #FFF 100%)`; spark `radial-gradient(58.33% 52.53% at 50% 50%, #E8899E 0%, #FFF 100%)`; uplifter `radial-gradient(58.33% 52.53% at 50% 50%, #FFA552 0%, #FFF 100%)`; explorer `radial-gradient(58.33% 52.53% at 50% 50%, #FFD55D 0%, #FFF 100%)`.
- Close `button.absolute.top-6.right-6.z-10.text-3xl.leading-none`: "×", 30px/30px, color #0a0a0a.
- Body `div.relative.flex.flex-1.flex-col.items-center.gap-6.px-4`: mascot `img.mt-6` 87x87 → header `flex flex-col items-center gap-4 px-4 lg:px-12` with H2 (`lg:desktop-h3 mobile-h3 font-serif`, Recoleta 40/48) and p (`lg:desktop-body mobile-body text-text-primary/80`, 20/30, color #2e2a42 at 80%) → items row `flex flex-col gap-6 lg:flex-row` (gap 24) of 4 `article.relative.flex.flex-1.flex-col.items-center.gap-2.5.rounded-3xl.bg-white.px-8.py-5 lg:min-h-[17rem] lg:min-w-[17rem]` (272x272, padding 20px 32px, radius 24). Each article holds an icon `absolute right-0 top-0 w-[2rem]` (32x32), h3 Recoleta 24px/33.8px `pr-12`, and p 16px/24px `pr-12`.
- Footer `footer.sticky.bottom-0.z-10.bg-white.p-4 lg:bg-transparent lg:p-6` with Button "Get Started For Free" in `max-w-[14rem]`.
- Content (card → mascot, title, subtitle, items [icon, title, text]):
  1. Survive the newborn stage → `worrier.svg`, "Lost in the newborn phase fog?", "You’re not alone. Riley can:" → puzzle "Get advice just for you" / "Riley takes pediatrician-vetted advice and applies it to your family's unique situation."; ruler "Keep track of everything" / "Easily track sleep, feedings, whatever, in the only app where your data is put to work."; handsTogether "Provide 24/7 support" / "Expert-backed support all day and night for all those “is this normal?” moments."; lightbulb "Predict naps and feeds" / "Riley's Golden Window™ helps you take the guesswork out of sleep and feeding."
  2. Get help with naps and sleep → `guide.svg`, "Tired of playing the nap guessing game?", "We’ve been there! Riley can:" → lightbulb "Take the guesswork out" / "Predict your baby's ideal naptime and bedtime with Riley's Golden Window™."; knight "Solve regressions, fast" / "Riley helps you handle regressions with expert-backed support."; ladder "Real-time adjustments" / "Riley learns your baby’s patterns and adjusts your support in real-time."; affectionate "Personalize routines" / "Create calm sleep routines that work for your family, now and in the long-term."
  3. Support baby development → `softie.svg`, "Worried about milestones?", "Yup, we've been there. Riley can:" → ruler "Track milestones" / "Track key milestones and prep you for what’s next for your little one."; curious (broken on live) "Help plan activities" / "Riley suggests age-appropriate, science-backed activities vetted by pediatricians."; music "Guide development" / "Riley helps spot patterns and trends to help guide healthy development."; independent "No comparisons" / "Riley gives personalized, data-driven support. No one-size-fits-all advice here."
  4. Navigating toddler tantrums → `spark.svg`, "Tantrums testing your patience?", "You’re not alone! Riley can:" → curious (broken) "Decode the why" / "Riley learns from what you’ve shared to help navigate meltdowns."; friendly (broken) "Match your needs" / "Riley suggests calming techniques that match your individual child’s needs."; books "Learn from what works" / "Riley helps track behaviors to spot what works - and what doesn't! - for your family."; heartParachute "Sanity reminders" / "Riley understands the science behind big toddler feelings - and guides you through it."
  5. Starting solid foods → `uplifter.svg`, "Not sure how to start solids?", "We know how that feels. Riley can:" → octopus "Guide you through it" / "Riley walks you through the what, when, and how of feeding."; everything "Personalized meal tips" / "Get meal tips based on your actual baby’s current routine."; ruler "Track feedings" / "Riley helps you keep track of different foods, reactions, and preferences."; heartParachute "Take the pressure off" / "Riley makes starting solids simpler, so you can focus on the joy, not the stress."
  6. Build a routine → `explorer.svg`, "Feeling like every day is chaos?", "It's totally normal! Riley can:" → calendar "Personalize routines" / "Riley creates a routine around your baby’s actual sleep and feed patterns."; magicWand "Grow with you" / "Needs change quickly with littles! Riley is the only app that grows with your family."; rocket "Proactively advise" / "Riley suggests age-appropriate activities based on your real-time data."; elephant "Take the guesswork out" / "Get expert, pediatrician-backed advice for every “What now?” moment."
- Modal assets are in `/assets/modal/mascots/` and `/assets/modal/icons/`.

---

## 5. Featurette ("Here's How Real Users Talk to Riley"; y 2292, h 1150 @1440)
- Outer `section.px-11.py-20.max-md:px-5`: padding 80px 44px (20px sides <768).
- Inner `section.relative.mx-auto.flex.w-full.max-w-[90rem].flex-col.items-center.gap-8.overflow-hidden.pt-8 lg:px-20 lg:py-10 2xl:px-4`: gap 32. Padding 40px 16px @1440 (2xl), 40px 80px @1280, 32px 0 0 <992.
- H2 `lg:desktop-h3 mobile-h2 text-center font-serif`: "Here's How `<i>Real</i>` Users`<br>`Talk to Riley:" Recoleta 40/48 (26/33.8 <992). The `<i>` uses the same family (synthetic italic).
- Card `div.relative.flex.flex-col.items-center.overflow-hidden.rounded-[30px].bg-orange-100.pt-8`: 1320x633 @1440, radius **30**, bg **#ff914d**, padding-top 32.
  - Bg image `img.absolute.left-0.top-0.h-full.w-full.scale-125` = **background-clouds.svg** (29b46e22), scaled 1.25.
  - Embla viewport `div.w-full.flex-1` → container `div.flex.h-full` (inline `transform: translate3d(...)`).
  - Slide `div.flex.w-full.flex-none.flex-col.items-center.justify-center.gap-6.px-4 lg:flex-row lg:gap-10`: padding 0 16px, gap 40 (24 <992).
    - Phone column `div.relative.order-2.mx-auto.aspect-[0.85].w-full.max-w-[511px] lg:order-1 lg:mx-0`: **511x601.2** (318x374 @390).
      - `phonebg.svg` (fill, `object-contain`, inline `top:8px; right:0; bottom:0; left:0`).
      - `div.absolute.-left-7.-top-0.flex.h-full.w-full.items-end.justify-center lg:-left-11` (left -44px ≥992, -28px below) holding the Rive canvas `pointer-events-auto relative z-10 h-full w-full`, 511x601 CSS px.
    - Right image `div.order-1.lg:order-2` → `img.my-auto.aspect-[0.89].w-[491px].object-contain max-md:max-w-full`: 491x551.7 @1440, 449x504.5 @1280, 318x357 @390. Below 992 the image sits **above** the phone.
  - Slides (Rive src, artboard, state machine, right image, alt):
    1. `/assets/animations/chat_module_meg.riv`, artboard `chat_module_meg`, SM `meg_chat_SM`, `meg.png` "Feeding help"
    2. `chat_module_seb.riv`, `chat_module_seb`, `seb_chat_SM`, `seb-and-daughter.png` "Seb & daughter testimonial"
    3. `chat_module_naina.riv`, `chat_module_naina`, `naina_chat_SM`, `naina.png` "Milestone celebration"
  - Rive config: `useRive({src, artboard, stateMachines, autoplay:true, layout:new Layout({fit:Fit.Cover, alignment:Alignment.Center})})`, `role="img" aria-label="Interactive Rive animation"`. The phone's chat content is canvas-rendered, so its text is **not measurable** (Rive). Use the .riv files.
- Controls (below the card, inside the inner section) `div.mx-auto.flex.w-full.items-center.justify-center.gap-8` (gap 32): two `button.rounded-full.bg-white/30.p-2.backdrop-blur` (29x29, padding 8, bg rgba(255,255,255,.3), `backdrop-filter: blur(8px)`), aria-labels "Previous slide" / "Next slide", icons featurette-prev/next.svg (13x13). No hover style.
- CTA below the inner section: `div.mx-auto.mt-8.flex.w-full.max-w-[14rem].flex-col.items-center` (margin-top 32) → Button "Talk to Riley" (224x56).

---

## 6. ClinicalBoard (y 3443, h 916.7 @1440)
- `section.text-text-primary.flex.flex-col.bg-white.px-24.py-16.max-md:px-5`: bg #fff, padding **64px 96px** (20px sides <768).
- Inner `div.mx-auto.flex.w-full.max-w-[90rem].flex-col.items-center.gap-16` (gap 64).
- Header `header.flex.w-full.flex-col.items-center.gap-10.text-center` (gap 40):
  - h3 `mobile-body lg:desktop-body`: "Our Clinical Advisory Board", Cadiz Regular 20/30 (16/24).
  - h2 `mobile-h2 lg:desktop-h3 font-serif`: "Designed with Experts, for Real Families", Recoleta 40/48 (26/33.8).
  - p `max-w-[30.75rem]` (492): 20/30. Text: **Our Clinical Advisory Board** includes **pediatricians, therapists,** and **specialists**, who help us keep Riley grounded in real, **evidence-based support**. (bold = `span.font-sans-bold`)
- Cards row `div.mx-auto.flex.w-full.flex-col.items-center.justify-center.gap-12.text-center lg:flex-row` (gap 48):
  - `article.flex.min-w-60.max-w-[22.625rem].flex-col.items-center.justify-center` (362 wide):
    - img `aspect-[0.99] w-[362px] max-w-full object-contain`: **362x365.7** (lilly.png / kate.png). Alts "Portrait of Dr. Lilly Jay" / "Portrait of Dr. Kate Roche".
    - `div.mt-8.flex.w-[334px].max-w-full.flex-col.items-center.justify-center.px-9.py-2` (margin-top 32, padding 8px 36px; 20px sides <768) → `div.flex.max-w-full.flex-col`: h3 `text-xl leading-tight text-slate-800` (Cadiz Regular **20px/25px**, #1d293d) and p `mt-4 self-center text-base leading-snug` (margin-top 16, **16px/22px**, #1d293d).
  - "Dr. Lilly Jay" / "PsyD, PMH-C, Perinatal Health"; "Dr. Kate Roche" / "MD, Child Neurology".

---

## 7. HowRileyWorks (y 4359, h 835.6 @1440; 899.4 @1280)
- `section.text-text-primary.bg-latte-100.flex.w-full.flex-col.items-center.p-20.max-md:px-5.2xl:px-4`: bg **#fcfbfa**, padding 80px 16px @1440 (2xl), **80px** @1280, 80px 20px <768.
- Inner `div.mx-auto.flex.max-w-[90rem].flex-col.gap-15.self-stretch` (gap **60**).
- H2 `lg:desktop-h2 mobile-h1 text-center font-serif`: "How Riley Works", Recoleta **60px/78px** (40/48 <992).
- Row `div.flex.w-full.flex-col.items-start.justify-center.gap-15 lg:flex-row lg:justify-between lg:gap-0`.
- Article `flex.min-w-60.flex-1.basis-0.flex-col.items-center.gap-8.px-12`: gap 32, padding 0 48px. Width 469.3 @1440, 373.3 @1280.
  - Image box `div.relative.flex.h-[8.75rem].w-full.items-center.justify-center` (**140px** tall). The img is `object-contain` 214 wide and **overflows** vertically: 214x195.3 (worrier-family.svg), 214x156.3 (guide-family.svg), 214x168 (spark-family.svg).
  - Text `div.flex.w-full.flex-col.items-center.gap-4.text-center lg:gap-8` (gap 32; 16 <992):
    - h3 `lg:desktop-h4 mobile-h3 whitespace-pre-line`: Cadiz Regular 24/33.8 ≥992; Recoleta 20/33.8 <992.
    - p `lg:desktop-body mobile-body`: 20/30 (16/24).
  - Content:
    1. "Built on science\nthat matters": "When answering your questions, Riley draws from the latest child development research, expert-reviewed sources that are vetted by our Clinical Advisory Board."
    2. "Powered by tech that learns\nand grows with you": "Once you start using Riley, it doesn’t just log or respond to you, it safely remembers. From tracking to what’s worked in the past, Riley learns from you to offer relevant guidance."
    3. "Clarity without ignoring\nyour individuality": "Every family is different, Riley gets that! You'll receive clear, science-backed guidance that respects your individual parenting style and real-life context."
- CTA `div.mx-auto.flex.w-full.max-w-[14rem]` → "Get Started For Free".

---

## 8. Testimonials (y 5195, h 1058 @1440; 1125.6 @1280)
- `section.w-full.bg-latte-150` (#f9f5f1), aria-labelledby testimonials-title.
- Inner `div.mx-auto.flex.w-full.max-w-[90rem].flex-col.items-center.gap-8.self-stretch.py-8 max-md:px-5 lg:gap-11 lg:px-70 lg:py-20`: ≥992 padding **80px 280px**, gap **44**. <992: padding 32px 0, gap 32 (390: 20px sides).
- Header `flex flex-col items-center gap-3 text-center lg:gap-8` (gap 32 / 12): p `lg:desktop-body sm:mobile-body` "Real Reviews, Real Families" (20/30); h2 `mobile-h2 lg:desktop-h3 font-serif` "Why Parents Love Riley" (40/48).
- Card `div.relative.flex.flex-col.items-center.gap-8.self-stretch.overflow-hidden.rounded-3xl.px-14.py-9.lg:px-40.lg:py-15.bg-violet-100`: 880x583 @1440, padding **60px 160px** (36px 56px <992), radius 24, bg #d7befc.
  - Embla `div.embla.mt-12.w-full.overflow-hidden` (margin-top 48) → `div.embla__container.flex.gap-6` (gap **24**).
  - Slide `figure.embla__slide.flex.shrink-0.basis-full.flex-col.items-center.gap-8.text-center.lg:basis-1/2`. Global CSS `.embla__slide{flex:0 0 100%;min-width:100%}` (and 50% at ≥1024px, but min-width 100% wins), so each slide is **100% of the viewport**: 560 @1440, 400 @1280, 656 @768, 238 @390. Gap 32.
    - `stars-5.svg` 198x38.
    - blockquote `desktop-h4 mx-auto max-w-3xl`: Recoleta **26px/33.8px** ≥992; Cadiz Regular 24px/33.8px <992. Text wrapped in curly quotes “…”.
    - figcaption `mt-10 flex flex-col items-center gap-4` (mt 40, gap 16): avatar 64x64 rounded-full object-cover; name `font-sans-semibold text-base` 16/24.
  - Slides:
    1. “10 days into having our newborn, we’ve already developed the habit of saying “Hm, not sure. Ask Riley” multiple times a day. Not sure what we’d do without having Riley to back our instincts.” | purple1.svg | Max L., Dad of Baby R (1 mo)
    2. “Riley offers calm and reassurance while Google makes me spiral. With my second, it feels like we’re starting over and have forgotten everything about the newborn phase but Riley’s here for all my questions” | purple2.svg | Meg F., Mom of Baby A (5 mos) and Baby H (2 yrs)
    3. “Compared to every other app, especially chat tools, Riley asks better questions and more relevant follow-ups based on my child’s age and the nuance of the moment - the end result is always more helpful.” | purple3.svg | Rebeckah R., Mom of Baby N. (7mo)
    4. “Riley’s tracking and recommendations are smart and proactive.  I love that it’s personalized and remembers details about my family without me having to myself.” (sic, double space and missing word as on live) | purple4.svg | App Store Review
    5. “I was traveling this week and *terrifyingly* my pump broke and I was panicking. Riley pulled through. Having a resource to text with at 1 am? 11/10.” | purple5.svg | R, Mom of Baby K. (5mo)
- Below the card: `div.flex.flex-col.items-center.gap-8` (gap 32) → arrows `div.flex.flex-row.gap-4` (gap 16; two 29x29 `rounded-full bg-white/30 p-2 text-xl leading-none backdrop-blur` buttons with review-prev/next.svg) → Button "Join the club" (197.7x56).

---

## 9. GradientBand: FeatureCards + ComparisonTable (y 6253, h 2078.2 @1440)
- Wrapper `div.flex.flex-col.items-center.gap-12.self-stretch.px-4.py-11.lg:px-8` with the radial gradient from §0.3. Padding **44px 32px** (16px sides <992), gap 48.

### 9.1 FeatureCards (`section`, 1376x780 @1440)
- `section.mx-auto.flex.max-w-[90rem].flex-col.items-center.gap-6.self-stretch.rounded-3xl.bg-white.px-2.py-4 max-md:px-5 lg:gap-12 lg:p-12`: bg white, radius 24, padding **48** (16px 8px <992; 16px 20px <768), gap 48 (24).
- Header `flex flex-col items-center gap-6 text-center` (gap 24): h3 `lg:desktop-body mobile-body` "Parenting is hard.`<br>`Riley makes it easier." (20/30, 2 lines); h2 `lg:desktop-h3 mobile-h2 font-serif` "One App for All Your Parenting Needs" (40/48).
- Cards row `div.flex.w-full.flex-col.items-start.gap-5.self-stretch.text-center lg:flex-row` (gap **20**).
- Card `article.flex.h-full.max-h-[25rem].flex-1.flex-col.px-8.pb-12.pt-8.min-w-60.basis-0.gap-7.rounded-3xl max-md:px-5`: 413.3 wide @1440 (360 @1280, full width <992), max-h 400, padding **32px 32px 48px**, gap **28**, radius 24.
  - img `max-w-100% h-full w-full self-center lg:h-[10.25rem] lg:w-auto` (164 tall ≥992; chat.svg renders 327x164, tracking/sparks 291.5x146.2 because of the max-h clamp; 656x320 @768; 278x139.4 @390).
  - Text `div.flex.w-full.flex-col.items-start.gap-4.self-stretch.text-center` (gap 16): h4 `lg:desktop-h4 mobile-h3 w-full text-center` (Cadiz Regular 24/33.8 ≥992; Recoleta 20/33.8 <992); p `mobile-body` (Cadiz Regular 16/24, `<strong>` synthetic bold 700).
  - Cards:
    1. bg **#ffa552**, chat.svg, "24/7 Personalized Support": "Real-time, science-backed advice tailored to **your baby's needs** and **your parenting style**—available **whenever** you need it (even at 3am)."
    2. bg **#d7befc**, tracking.svg, "Smart, Predictive Tracking": "Riley doesn't just store your data, it **learns and grows with you**. Track sleep, feed, diapers, development and more to stay on top of what's next for your baby."
    3. bg **#ffd55d**, sparks.svg, "Tips Tailored Just for You": "No more endless Googling. Riley gives you **helpful tips made just for your family**—so you can parent with a little more ease (and a lot less guesswork)."
- CTA `div.flex.max-w-[14rem]` → "Get Started For Free".

### 9.2 ComparisonTable (`section`, 1376x1162 @1440)
- `section.mx-auto.w-full.max-w-[90rem].rounded-3xl.bg-white.px-2.py-4 lg:p-12` (padding 48; 16px 8px <992; 16px 20px <768).
- Header `mt-4 flex flex-col items-center gap-3 text-center lg:gap-8` (mt 16, gap 32/12): p "Designed with Real Parents in Mind" (20/30); h2 "Why Riley Stands Out" (40/48); `div.prose.max-w-[25rem]` (400) → p (margin 20px 0, Cadiz Regular **16px/28px**, #364153): "See how Riley outshines other parenting tools with **intelligent features** and **tailored advice**. It’s the **one-stop-shop** for all your parenting needs!" (strong: fw 600, #101828).
- Table wrapper `div.mx-auto.mt-6.w-full.max-w-6xl.lg:mt-12` (max-w 1152, mt 48; 24 <992) → `div.bg.overflow-x-auto.rounded-2xl.p-6.px-3.lg:p-6` (inline `background-color: var(--background)` = #f9f5f1, radius 16, padding 24 ≥992 / 24px 12px below).
- `table.w-full.border-separate.border-spacing-y-4.text-left`: border-spacing **0 16px**. Width 1104 @1440.
  - thead row `text-center`: th `px-4 font-bold` "Feature/Benefit" (16/24, fw 700); then 7 th `px-4 font-normal` each with a `span`: Riley | Google Search | Reddit | ChatGPT | Claude | Other Tracking Apps | Podcasts, Books, & Blogs (Cadiz Regular 16/24; multi-word labels wrap to 2 lines). Column widths @1440: 340.5, 78, 114.6, 80, 98.1, 83.5, 144.5, 164.8.
  - td `mobile-h4 lg:desktop-h4 border-l border-[#000] bg-white px-6 py-3 text-center shadow-sm`: padding 12px 24px, white, border-left **1px #000**, `shadow-sm`. First td: `rounded-l-2xl border-none text-left`, Cadiz Regular 24px/33.8px. Last td `rounded-r-2xl`. Row heights 57.8 (row 1), 91.6 (rows 2–5).
  - Connector: every td except the first has `::before{content:"";position:absolute;left:-1px;top:100%;width:1px;height:1rem;background:#000}`, hidden on the last row. This draws the vertical rules through the 16px row gaps.
  - Matrix (F = `table-check-filled.svg` purple 29x29, E = `table-check-empty.svg` outline 31x30), columns Riley, Google, Reddit, ChatGPT, Claude, Other Tracking, Podcasts:
    - 24/7 Instant Answers: F F F F F E E
    - Expert-Vetted, Science Backed Support: F E E E E E F
    - Guidance Tailored to You & Your Family: F E E E E E E
    - Proactively Turns Tracking Into Tips: F E E E E E E
    - All-In-One Tracking & Support: F E E E E F E
  - ≤960px: td padding 15px 10px, max-width 100px, font-size 14px !important, svg width 15px. th height 140px, vertical-align bottom, position relative, header span absolute, `transform: rotate(-90deg) translate(14px,20px)`, transform-origin center left, 13px, nowrap (vertical labels). The table is 398px wide @390 and scrolls horizontally in its wrapper.
- CTA `div.mx-auto.mt-12.flex.w-full.max-w-[15rem]` → "Join Riley—early, easy, free" (240x56).

---

## 10. FaqClouds (y 8331, h 900 @1440; 1100 ≤960)
- `section.FaqClouds_faq-clouds.flex.min-h-[900px].w-full`: position relative, background `radial-gradient(rgb(165,201,242) 0, #f9f5f1 70%) no-repeat`, size 200% 100%, position 50% 50%, transition .3s ease. min-height **900** (1100 ≤960).
- Title row `div.mh-full.relative.flex.w-full` → `div.mx-auto.flex.w-full.max-w-[90rem].items-center.justify-center` → h2 `desktop-h2 mx-auto max-w-[50rem] text-center` "We’re Here to Make Things Clear": **80px / 104px** (module CSS `font-size:80px;line-height:1.3`), Recoleta ≥992, color **#0a0a0a**, position relative, z 1, 800x208 (2 lines), vertically centered. ≤960: 40px/52px, padding 0 16px, Cadiz Regular below 992.
- Items container `div.absolute.h-full.w-full` → 5 `details.FaqClouds_faq-clouds-item.max-w-xs.cursor-pointer.rounded-3xl.bg-white.p-4.shadow-md.transition-all.duration-300`:
  - position absolute, z 1, **width 295px**, max-w 320, padding 16, radius **24px 24px 0 24px** (bottom-right square), shadow-md, transition `all .35s ease-in-out`.
  - summary `flex list-none items-center gap-3 font-bold` (gap **16** from the module), Cadiz Regular 16px/24px fw 700 (synthetic), #0a0a0a: avatar img 40x40 rounded-full object-cover; question span; `faq-plus.svg` 19x19 (`margin-left:auto; flex:0 0 19px; transition:.45s ease`).
  - Answer `div.prose.mt-2.max-w-none.px-3` (mt 8, padding 0 12px): p 16px/28px, margin 20px 0, text in `span style="color: rgb(0,0,0)"`. Then `div.flex.items-center.gap-2` (gap 8): Button "Learn More" → `/pricing`, and `riley-up.svg` img `mb-2 mt-0 h-[5rem] w-auto` (98.3x80).
  - Desktop positions (top/left as % of the section): 1: 27%/12%; 2: 13%/35%; 3: 24%/61%; 4: 63%/61%; 5: 72%/30%. (A 6th rule, 60%/7%, exists but has no item.)
  - ≤960 positions: 1: 5%/20% (max-w 80%); 2: 16%/5% (90%); 3: 28%/15% (80%); 4: 75%/7% (90%); 5: 63%/20% (90%).
  - Content (portrait → Q → A):
    1. 4.png → "How do I know I can trust Riley?" → "Riley's advice is grounded in the latest pediatric research and expert knowledge. We work closely with pediatricians, child development specialists, and parenting experts to ensure our information is accurate and up-to-date. Plus, Riley learns from your experiences, becoming more personalized and helpful over time."
    2. 5.png → "How is Riley different from ChatGPT or other parenting apps?" → "Riley isn’t just another chatbot. It learns from your baby’s age, symptoms, tracking history, and anything that's worked for your family in the past. Delivering expert-vetted advice that fits your family, not just “most families.”"
    3. 3.png → "What can’t I ask Riley?" → "Riley gives science-backed, personalized parenting support - but it’s not a doctor, therapist, or emergency service. It’s here for guidance on sleep, feeds, development, routines, and real-life questions - not for diagnosing medical conditions."
    4. 2.png → "Are you going to keep my kids’ data private?" → "Your family's privacy is our top priority. We use bank-level encryption to protect your data, and we never share your information with third parties. Riley's personalized advice is generated just for you, based on the information you choose to share. You're always in control of your data, and you can delete it at any time. Riley was built to support your parenting - not to profit from your info."
    5. 6.png → "Do I need to track everything for Riley to work?" → "Nope. Tracking helps tailor the experience, but Riley gives helpful, relevant support even if you skip a day - or a week."
  - Open state (`details[open]`): width 350 (capped by max-w-xs, so measured **320**), z 100. ≥961: `top:50% !important; left:50% !important; transform:translate(-50%,-50%)` (centered; measured 320x488 for item 1). ≤960: `width:100% !important; left:5% !important; max-width:90% !important`. Plus icon `rotate(135deg)`. While any item is open the section gets `.blurred` (§14 M9).
- Background clouds `div.FaqClouds_faq-clouds-bg` (absolute, 100%x100%, overflow hidden), 5 inline SVGs (`faq-cloud-1..5.svg`: 452x276 gradient opacity .65; 326x199 gradient .95; 244x149 white .5; 383x167 white .5; 401x246 gradient), each absolute with `transition: 2.55s ease` and the floating animation (§14 M8).
  - Initial positions: 1: top 30% left 20% (mobile left -50%); 2: 60%/44% (mobile left -50%); 3: 18%/55% (mobile 30%/70%); 4: 69%/15% (mobile 75%/10%); 5: 31%/65% (mobile top 50%).
  - `.clear-skies` positions: 1: 0/-5%; 2: 70%/-5%; 3: 10%/80%; 4: 32%/-10% (mobile left 94%); 5: 51%/90%. ≤960 with clear-skies: svg opacity **.05**.

---

## 11. BlogTeaser (y 9231, h 1032 @1440)
- `section.mx-auto.flex.w-full.max-w-[90rem].flex-col.items-center.justify-center.gap-8.self-stretch.rounded-3xl.bg-white.px-4.py-8 lg:px-9 lg:py-25`: bg white, radius 24, padding **100px 36px** (32px 16px <992), gap 32.
- Header `flex flex-col items-center gap-4 lg:gap-9` (gap 36/16): h4 `lg:desktop-body sm:mobile-body` "Insightful Reads for Modern Parents" (20/30); h2 "Explore the Riley Blog" (40/48).
- Category nav `nav.w-full.overflow-x-auto.px-2.py-4.sm:overflow-visible` (padding 16px 8px) → `ul.mobile-body.flex.w-max.items-center.justify-center.gap-4.sm:mx-auto.sm:w-auto` (gap 16) → li → `a.font-sans-bold.whitespace-nowrap.rounded-[40px].px-4.py-1.5.text-sm.font-bold.leading-5.text-slate-800.transition-opacity.hover:opacity-80`: inline, padding 6px 16px, radius 40, 14px/20px fw 700, #1d293d.
  - Development `/blog/development` bg #ffd6a7; Feeding `/blog/feeding` #f1f5f9; Health `/blog/health` #ffc9c9; News `/blog/news` #f1f5f9; Pregnancy `/blog/pregnancy` #f1f5f9; Sleep `/blog/sleep` #e7e5e4.
- Cards (≥640): `section.mt-8.flex.w-full.flex-wrap.justify-center.gap-6` (mt 32, gap 24) → `article.flex.w-full.max-w-[18rem].flex-col.items-center.gap-7` (288 wide, gap 28) → `a.group.w-full` →
  - `div.relative.w-full.overflow-hidden.rounded-[35px].aspect-[3/4].lg:aspect-auto.lg:h-[22rem]`: radius 35, **288x352** ≥992, 288x384 (3:4) below.
  - img fill `object-cover transition-transform duration-300 group-hover:scale-105` (sizes "(max-width: 639px) 45vw, 270px").
  - h4 `mt-4 text-center font-serif text-[0.875rem] leading-[1.1375rem] underline lg:text-[1.25rem] lg:leading-[1.625rem]`: mt 16, Recoleta **20px/26px** underline #2e2a42 (14px/18.2px <992).
  - Posts: "Baby Witching Hour: What It Is, When and Why It Happens, and How to Manage It" → `/blog/sleep/baby-witching-hour` (3dd009c0…jpeg); "1 Month Old Sleep Guide: Bedtime and Nap Schedules" → `/blog/sleep/1-month-old-sleep-guide` (6ec23763…jpeg); "16 Month Old Sleep Schedule: How Much Should a 16 Month Old Sleep?" → `/blog/sleep/16-month-old-sleep-schedule` (8fe3a7b3…jpeg).
- ≤639px (JS `matchMedia('(max-width: 639px)')`): the cards render as a horizontal scroller `section.scrollbar-thin.mt-8.w-full.overflow-x-auto` → `div.flex.snap-x.snap-mandatory.gap-2.pr-4` (gap 8, pr 16) → `div.shrink-0.grow-0.snap-start` with inline `flex-basis: calc(50% - 4px)` (167 wide @390; image 167x222.7). The embla hook uses `{align:'start', containScroll:'trimSnaps', loop:false}`.
- CTA `div.mt-8.flex.flex-col.items-center.gap-20` → Button "Explore the blog" (223.7x56).

---

## 12. FinalCta (y 10263, h 708 @1440; 786 @1280; 440 @768; 536 @390)
- `section.relative.flex.w-full.flex-col.items-center.self-stretch.overflow-hidden.px-8.py-20.pb-40 lg:px-[20rem] lg:py-[14rem]`: padding **224px 320px** ≥992; 80px 32px 160px below.
- Bg `img.absolute.top-0.-z-10` = **background-clouds(1).svg** (0c94200b, 1774x826), full width (1440x670.5 @1440).
- Content `div.flex.w-full.flex-col.items-center.justify-center.gap-12.overflow-hidden` (gap 48): h2 `lg:desktop-h2 mobile-h1 text-center font-serif` "We are raising a generation`<br>`of confident parents." Recoleta **60px/78px** (40/48), 710.6x156 @1440; then `div.flex.max-w-[20rem]` → Button "Get support that gets you" (289.1x56).
- Mascots `div.-bottom-18.absolute.left-1/2.z-0.flex.h-[12rem].min-h-24.w-[42.5rem].max-w-full.-translate-x-2/4 lg:-bottom-14`: **680x192**, centered, bottom **-56px** ≥992 (-72 below), clipped by the section → `mascots.svg`. 390x192 @390.

---

## 13. SiteFooter (y 10971, h 493.6 @1440)
- `footer.z-30.mx-auto.flex.w-full.max-w-[90rem].flex-col.items-center.justify-center.gap-16.self-stretch.overflow-hidden.px-8.py-12 lg:gap-12 lg:px-[3.75rem] lg:py-[5.5rem]`: padding **88px 60px** ≥992 (48px 32px below), gap **48** (64 below). Transparent bg (page latte shows through).
- Top row `div.flex.w-full.flex-col.items-center.justify-between.gap-8.self-stretch md:flex-row md:flex-wrap md:justify-between lg:max-w-[1440px] lg:flex-nowrap` (gap 32; 1320x142 @1440):
  1. Newsletter `section.flex.w-full.flex-1.flex-col.items-center.justify-center.gap-6 lg:max-w-[28.75rem] lg:items-end` (337.3 wide, gap 24):
     - p `font-serif text-[1.25rem] leading-[1.625rem] text-center lg:text-left`: "Stay in the loop with Riley's newsletter." Recoleta 20/26.
     - form `flex w-full max-w-[28.75rem] items-center justify-between rounded-[2rem] border border-solid border-white bg-white pl-6`: 64px tall, radius 32, 1px white border, padding-left 24. Input `type=email placeholder="Email"` Cadiz Regular 16/24 #2e2a42, transparent, no outline. Button `font-sans-regular desktop-body ... rounded-[78.641px] bg-purple-100 px-6 py-4 text-white` "Sign up": 116.5x62, Cadiz Regular **20px/30px**, bg #5934c5, padding 16px 24px, `disabled:opacity-60`. No hover style.
  2. `footer-divider.svg` 1x142 (`hidden lg:flex`).
  3. Nav `div.flex.gap-x-16` (column gap 64) of two `div.flex.flex-col.gap-y-6` (row gap 24). Links `a` → `span.font-sans-semibold.text-[1rem].text-purple-100` (Cadiz SemiBold face 16/24, #5934c5, no hover): col 1 Blog `https://rileyapp.com/blog`, Pricing `/pricing`, Editorial Process `/editorial-process`; col 2 Privacy Policy `/privacy`, Terms of Service `/tos`, Support `/support` (all absolute `https://rileyapp.com/...`).
  4. Divider svg.
  5. "Get the App" block `flex flex-col items-center justify-center gap-4 lg:items-start` (gap 16): p `desktop-h4` "Get the App" Recoleta 26/33.8; link `https://rileyapp.onelink.me/JNxh/ln83navr` → `app-store-badge.svg` 153x52.
- Bottom `div.flex.w-full.flex-col.items-center.gap-8` (gap 32): `footer-logo.svg` 118x76, then p `font-sans-regular text-[0.875rem] leading-[1.225rem]` "© 2025 Riley" (14/19.6, #2e2a42).
- <768: everything stacks centered. Dividers are hidden. The form widens to 460 @768 and is full width (326) @390.

---

## 14. Motion inventory

| # | Element | Trigger | Properties | Duration / easing / delay | Notes |
|---|---|---|---|---|---|
| M1 | Site header | page load | `opacity 0→1` (framer `initial/animate`) | 0.5s; framer default tween easing (exact curve **UNVERIFIED**) | |
| M1b | Desktop nav (Blog, What's New?, divider, CTA) | page load | container `opacity 0→1` with `staggerChildren .2`, `delayChildren .1`; each child `opacity 0→1, y 20→0` | child 0.6s, ease **cubic-bezier(0,0,0.58,1)** (framer `easeOut`) | stagger 200ms, 4 children |
| M2 | Header sticky | scroll, `window.scrollY > 54` (scroll listener) | header switches from `relative` to `fixed top-0 left-0 right-0` with `shadow-md` (0 4px 6px -1px #0000001a, 0 2px 4px -2px #0000001a) and `backdrop-filter: blur(12px)`. bg stays transparent (gradient from an undefined color). A spacer div with the header's offsetHeight (80px) is inserted. | `transition-all 300ms cubic-bezier(.4,0,.2,1)` | stays visible on scroll up and down (no hide-on-scroll); z 100 |
| M3 | Hero clouds (horizontal) | load, infinite loop | `transform: translateX(-645px) → translateX(calc(100vw + 645px))` (keyframes injected at runtime; measured end 2085px @1440, 1925px @1280) | floatSlow **100s linear infinite** (alt delay -50s); floatMedium **85s** (alt -42.5s); floatFast **50s** (alt -15s) | each pair = one normal + one `.cloud-alt` (negative delay) so clouds are spaced half a cycle apart |
| M3b | Hero parallax layers | scroll | translateY: L1 0→-20%, L2 0→-35%, L3 0→-50%, L4 0→-100% plus scale 0.8→1.2 | linear in progress `p = clamp(scrollY / (heroTop + heroHeight), 0, 1)` (react-scroll-parallax `shouldAlwaysCompleteAnimation`). Measured p = scrollY/964.3 @1440: at 300px L1 -6.22%, L4 -31.1% scale .924; complete at ≥964 | L1–L3 are "expanded" (top inset = -range × banner height) so no gap shows |
| M4 | Press marquee | load, infinite | `translateX(0) → translateX(calc(-100% - var(--gap)))`, --gap 16px | **20s linear infinite** | 4 copies, edge mask 0–20% / 80–100%; no pause on hover |
| M5 | Family marquee | load, infinite | same keyframes, `animation-direction: reverse` | **50s linear infinite reverse** | 4 copies |
| M6 | Featurette carousel | click prev/next, drag | embla `{loop:true}` (embla defaults otherwise: duration 25, align center, dragFree false) | embla default | no autoplay; Rive area has `data-embla-skip-drag` |
| M6b | Rive phone chats | autoplay on mount | state machines `meg_chat_SM` / `seb_chat_SM` / `naina_chat_SM` | defined inside the .riv | canvas, fit Cover, align Center |
| M7 | Testimonials carousel | click prev/next, drag | embla `{loop:true}` | embla default | no autoplay |
| M8 | FAQ bg clouds | load, infinite | keyframes `FaqClouds_floating`: 0% translate(0); 20% (6px,-4px); 40% (-5px,8px); 60% (8px,5px); 80% (-6px,-6px); 100% translate(0) | **10s ease-in-out infinite alternate-reverse**; delays -2s, -4s, -6s, -8s, -1s | |
| M8b | FAQ "clear skies" | IntersectionObserver on the clouds bg, **threshold 0.2**, then `setTimeout 1000ms` | adds `.clear-skies` → clouds move to the edges (top/left change) | `transition: 2.55s ease` | fires once (state never resets) |
| M9 | FAQ open | click summary (`details` toggle) | item: width, top/left → 50%/50% + translate(-50%,-50%) (desktop) | `transition: all .35s ease-in-out` | section `.blurred`: bg clouds `filter: blur(5px)` (transition filter .3s), other closed details `blur(5px)` + pointer-events none, h2 `blur(5px)` opacity .3 (.3s ease); plus icon rotate(135deg) over .45s ease |
| M10 | Primary buttons | hover / mousedown | bg #5934C5 → #7A55FD (hover) → #5A20E1 (active) | `all 300ms cubic-bezier(.4,0,.2,1)` | JS inline style |
| M11 | Nav links, blog pills, mobile-menu items | hover | opacity 1 → .8 | 150ms cubic-bezier(.4,0,.2,1) | |
| M12 | Superpower cards | hover | bg #fff → #f9fafb | 150ms cubic-bezier(.4,0,.2,1) | click opens modal (no animation) |
| M13 | Blog card image | hover on card link (`group`) | `scale: 1 → 1.05` | 300ms cubic-bezier(.4,0,.2,1) | parent clips (radius 35) |
| M14 | Mobile menu panel | toggle | `y: 100% → 0` (exit back to 100%) | 0.25s framer tween | backdrop blur 8px; panel blur 24px; body scroll locked |
| M15 | Mobile Blog sub-links | expand | `opacity 0→1, y -10→0` | framer default | |

No scroll-reveal or whileInView animations: computed styles of every element were identical before and after scrolling the full page. No video. No CSS `position: sticky` on the page. The only fixed element is the header after 54px of scroll.

CSS keyframes in the saved CSS: `enter`, `exit` (tailwindcss-animate, unused here), `marquee`, `marquee-vertical` (unused), `pulse`, `spin` (unused here), `FaqClouds_floating__oOvg0`. Runtime-injected `<style id="cloud-animations">` adds `floatSlow`, `floatMedium`, `floatFast` and `twinkle` (0%,100% opacity 1; 50% .3; 4s ease-in-out, `.animate-twinkle-delayed` -2s, `-more` -3s; not used on this page). Keyframe bodies:
```css
@keyframes marquee{0%{transform:translate(0)}to{transform:translateX(calc(-100% - var(--gap)))}}
@keyframes marquee-vertical{0%{transform:translateY(0)}to{transform:translateY(calc(-100% - var(--gap)))}}
@keyframes pulse{50%{opacity:.5}}
@keyframes spin{to{transform:rotate(1turn)}}
@keyframes FaqClouds_floating{0%{transform:translate(0)}20%{transform:translate(6px,-4px)}40%{transform:translate(-5px,8px)}60%{transform:translate(8px,5px)}80%{transform:translate(-6px,-6px)}to{transform:translate(0)}}
@keyframes floatSlow{0%{transform:translateX(-645px)}100%{transform:translateX(calc(100vw + 645px))}} /* same for floatMedium/floatFast */
@keyframes twinkle{0%,100%{opacity:1}50%{opacity:.3}}
```

---

## 15. Per-breakpoint section heights (px)
| Section | 1440 | 1280 | 768 | 390 |
|---|---|---|---|---|
| AnnouncementBar | 54.4 | 54.4 | 0 | 0 |
| Hero (incl. header + press strip) | 909.9 | 909.9 | 1483.2 | 1449.9 |
| PersonalizationMarquee | 664 | 664 | 488 | 760 |
| Superpowers | 664 | 746.8 | 931.6 | 947.8 |
| Featurette | 1150.2 | 1150.2 | 1649.4 | 1228 |
| ClinicalBoard | 916.7 | 916.7 | 1403.1 | 1436.7 |
| HowRileyWorks | 835.6 | 899.4 | 1486.8 | 1654.8 |
| Testimonials | 1058 | 1125.6 | 816 | 1076.6 |
| GradientBand | 2078.2 | 2078.2 | 2595.2 | 2726.6 |
| FaqClouds | 900 | 900 | 1100 | 1100 |
| BlogTeaser | 1032 | 1032 | 1306.6 | 721.3 |
| FinalCta | 708 | 786 | 440 | 536 |
| Footer | 493.6 | 493.6 | 553.6 | 713.4 |

## 16. Gaps / UNVERIFIED
- Phone chat UI in the featurette is canvas (Rive). Its content and timing live inside the .riv files and cannot be measured in the DOM.
- Exact framer-motion easing for the header opacity fade (M1) and the mobile-menu slide (M14): only durations are known from source.
- CTA destinations other than those listed in §0.6.
- Mobile-menu Blog sub-category list (comes from `/api/get-blog-categories` at runtime).
- `/icons/curious.svg` and `/icons/friendly.svg` are broken on the live site (soft 404), so two modal icons render as broken images on the original.
- "What's New?" opens a changelog modal (Sanity content). Not specced.
- Raw measurement dumps (JSON) for all four widths are kept in `/Users/riyaghosh/V3/rileyapp/.playwright-mcp/` (d1440.json, d1280.json, d768.json, d390.json, content1440.json, network.txt) for lookups.
