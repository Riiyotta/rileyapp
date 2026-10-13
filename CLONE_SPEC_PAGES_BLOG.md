Source: https://rileyapp.com/

# Riley blog and text pages: clone spec

Recon date: 2026-10-13. Measured live with an isolated Playwright Chromium at 1440x900, 768x1024 and 390x844. Article bodies were measured on 5 articles, chosen from a block-type tally over all 221 posts:
- A1 `/blog/sleep/baby-witching-hour`: promo unit, bullets, citations, h2/h3, sources, Amanda as author, no reviewer
- A2 `/blog/sleep/23-month-old-sleep-schedule`: medical reviewer, Editor's Note
- A3 `/blog/news/introducing-the-new-riley`: inline images
- A4 `/blog/pregnancy/maternity-leave-planning-what-to-do-before-baby-arrives`: nested bullets
- A5 `/blog/news/the-ultimate-guide-to-free-baby-tracker-apps`: downloadable image

Values are computed styles or getBoundingClientRect results unless marked **UNVERIFIED**. Global tokens, fonts, `Button`, `SiteHeader`, `AnnouncementBar`, `FinalCta` and `SiteFooter` are specified in `CLONE_SPEC.md` and are not repeated here.

The blog CMS is **Sanity** (`cdn.sanity.io/images/antwkw01/development/...`), not Storyblok. Legal pages are Storyblok stories that hold one Termly embed (see §5).

---

## 0. Cross-template facts

### 0.1 Colour conversions used below (computed oklch → hex)
| Computed | Hex | Tailwind name |
|---|---|---|
| rgb(46,42,66) | #2e2a42 | `text-primary` (existing) |
| oklch(0.145 0 0) | #0a0a0a | `ink` (existing). Body default. Every `text-brand-*`, `text-text-secondary` and `text-text-tertiary` class on these pages is **undefined** on the live CSS, so those elements fall back to this colour. |
| oklch(0.21 0.034 264.665) | #101828 | gray-900 (prose links, prose headings/bold on text pages) |
| oklch(0.373 0.034 259.733) | #364153 | gray-700 (list items, promo text, sources) |
| oklch(0.551 0.027 264.364) | #6a7282 | gray-500 (inactive category tab, search snippet) |
| oklch(0.707 0.022 261.325) | #99a1af | gray-400 (breadcrumb chevron) |
| oklch(0.872 0.01 258.338) | #d1d5dc | gray-300 (search input border, copy-link hover bg) |
| oklch(0.928 0.006 264.531) | #e5e7eb | gray-200 (tab bar bottom border, share button border) |
| oklch(0.922 0 0) | #e5e5e5 | default border colour (pagination pills, "See All >") |
| rgb(217,217,217) | #d9d9d9 | TOC progress track |
| rgb(123,99,245) | #7b63f5 | promo button base, chevron strokes |
| rgb(89,52,197) | #5934c5 | `purple-100` (search icon, input focus border, cookie OK button) |

**Important quirk:** the live CSS has no `brand-*`, `text-secondary`, `text-tertiary`, `bg-brand-*`, `font-sansSemibold`, `text-opacity-*`, `border-opacity-*` or `bg-greenGradient`-hover rules (Tailwind v4 dropped them). This has these effects:
- `font-sansSemibold` renders as **Cadiz Regular** (inherited `sansRegular`). Only `font-sansBold` (Cadiz Bold) and `font-sansRegular` exist.
- Every `hover:text-brand-*`, `group-hover:text-brand-400` and `hover:bg-brand-*` does nothing visible.
- The active-tab underline (`bg-brand-500`), the TOC progress fill and the Editor's Note bg (`bg-brand-100`) are **transparent**.
- `border-text-primary border-opacity-20` renders as a **solid #2e2a42 1px** border.

Clone what is rendered. Each affected place is called out below.

### 0.2 Category tag map (from the JS `CategoryTag` component)
| category | bg | icon (local) | icon natural size |
|---|---|---|---|
| sleep | `#EACDFF` | `/assets/blog/icons/moon.svg` | 28x28 |
| feeding | `#FFEAA7` | `/assets/blog/icons/bowl.svg` | 28x29 |
| development | `#E0FFE0` | `/assets/blog/icons/duck.svg` | 28x28 |
| news | `#CFF6FF` | `/assets/blog/icons/lightbulb.svg` | 28x29 |
| health | `#FFC7C3` | `/assets/blog/icons/first-aid.svg` | 28x25 |
| pregnancy | `#8DE8B2` (`--category-pregnancy`) | `/assets/blog/icons/octopus.svg` | 28x28 |
| default | gray-200 | none | |

- The tag is `div.flex.items-center.justify-start.gap-1.rounded-full.px-4.py-2` (padding 8px 16px, gap 4px, radius 9999). Icon alt is `"<category> icon"`. Label `span` is Cadiz Regular 16/24 #2e2a42.
- Label text = the post's **subcategory**, for example "Sleep problems", "Milestones", "Formula", "Behind Riley" or "Product feature". It falls back to the category title.
- `size="large"`: icon 24x24, used in the featured banner (152x40.9). `size="small"`: icon 16x16, used on grid cards (for example 165.6x40).
- The same colour is used as the bg of the current-page breadcrumb pill on articles.
- These are **not** the homepage `BlogTeaser` pills (different colours and typography).

### 0.3 Which global chrome appears per route (measured)
| Route | AnnouncementBar | SiteHeader | CookieConsent | FinalCta | SiteFooter |
|---|---|---|---|---|---|
| `/blog`, `/blog?page=N` | yes (54.4) | yes | yes | yes | yes |
| `/blog/<category>` | **no** (header at y 0) | yes | yes | yes | yes |
| `/blog/<category>/<slug>` | **no** | yes | yes | yes | yes |
| `/editorial-process` | yes | yes | yes | **no** | yes |
| `/tos`, `/privacy`, `/cookies` | yes | yes | yes | **no** | yes |

The SiteHeader is identical to the homepage one: 80px tall. Past 54px of scroll it becomes `fixed top-0` with shadow-md and `backdrop-blur 12px`, which was verified at mid-article. `FinalCta` is pixel-identical to the homepage: 708 tall @1440, 440 @768, 536 @390, same assets.

### 0.4 `<title>` / meta patterns
| Template | `<title>` | meta description | canonical | og / twitter |
|---|---|---|---|---|
| `/blog` (and `?page=N`) | `Riley Articles \| Riley` | "Riley is an expert in pediatric development, specializing in parenting support and baby tracking. From sleep schedules and bedtime routines to feeding schedules…" (site-level) | `https://www.rileyapp.com/blog` (also on page N) | site defaults (`og:title` "Riley – Baby Tracker & Child Development Expert", `og:image` `/opengraph-image.png` 1200x630) |
| `/blog/<cat>` | `<Category Title> - Blog \| Riley`, e.g. `Sleep - Blog \| Riley` | site default ("Riley learns and grows with your family…") | `https://www.rileyapp.com/blog/<cat>` | site defaults |
| article | `<seoTitle> \| Riley` (`seoTitle` stored as `seoTitle` in blogPosts.json, already suffixed) | `post.description` (= `excerpt`) | `https://www.rileyapp.com/blog/<cat>/<slug>` | `og:title` = title; `og:description` = description; `og:image` = full Sanity URL (no transform); `twitter:card` summary_large_image; `twitter:title` / `twitter:description` stay site defaults |
| `/editorial-process`, `/tos`, `/privacy`, `/cookies` | `Riley – Baby Tracker & Child Development Expert` (site default) | site default | `https://www.rileyapp.com/` (site root, a bug on the original) | site defaults |

JSON-LD on every page: Organization + WebSite (with SearchAction `https://rileyapp.com/blog?search={search_term_string}`). Articles add:
- `Article`: headline, description, image[], author {Person, name, url `/blog/author/<slug>`}, publisher, datePublished, dateModified, url, mainEntityOfPage, articleSection = category title, keywords `[category, subcategory]`.
- `BreadcrumbList`: Home → Blog → Category → Title.

### 0.5 Date format
Card date and article "Updated:" both render **`updatedAt`** in the viewer's local timezone as `D Mon YYYY` (en-GB short month, no comma), for example "8 Apr 2025".
- Confirmed: `2025-10-01T19:44Z` shows "2 Oct 2025" in IST. `2025-07-23T19:41Z` shows "Updated: 24 Jul 2025".
- When `updatedAt` is null (1 post), no date is shown.
- Read time renders as `"<n> min read"` only when `readingTime` is set (52/221 posts).
- The September abbreviation ("Sep" vs "Sept") is **UNVERIFIED**.

### 0.6 CookieConsent (global, NEW, `react-cookie-consent`; not covered by the homepage spec)
- `div.CookieConsent` inline style:
  - `position:fixed; left:60%; bottom:0; width:40%; z-index:9999`
  - `display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:1rem`
  - `background:rgba(255,255,255,.9); backdrop-filter:blur(6px); color:#2e2a42`
  - `border-top-left-radius:30px; border-top-right-radius:30px; padding:.75rem 1rem; font-size:.875rem`
  - `box-shadow:0 4px 16px rgba(0,0,0,.06)`
- @1440: 576x91 at x 864. @390: 156px wide (40% of the viewport), and the text block overflows to the left of it. This is the original's behaviour.
- Text block `style="flex:1 0 300px;margin:0"`: "By using this site, you accept cookies for analytics.&nbsp;" + `a.underline` "Learn more" → `/privacy`. Cadiz Regular 14/21.
- Button `#rcc-confirm-button`, `aria-label="Accept cookies"`, text "OK": bg #5934c5, white, radius 24, padding .5rem 2rem, margin 15px, weight 600, 14px, nowrap. 84.7x37.
- No entry animation. It hides on click (library default cookie `CookieConsent`; name **UNVERIFIED**).

---

## 1. REUSE / NEW matrix

### 1.1 `/blog` index (also `/blog?page=N`)
| # | Section | Tag |
|---|---|---|
| 1 | Announcement | `REUSE AnnouncementBar` (no changes) |
| 2 | Header | `REUSE SiteHeader` (standalone, not inside `Hero`; same sticky behaviour) |
| 3 | Mascot + "Riley Articles" + subtitle + books | `NEW BlogIndexHero` |
| 4 | Search box + results dropdown | `NEW BlogSearch` (props: `className`, `widthClass`; reused on articles) |
| 5 | Category tabs | `NEW BlogCategoryTabs` (prop `active`: 'all' or a category slug). Not the BlogTeaser pills. |
| 6 | Featured banner | `NEW BlogFeaturedCard` (desktop horizontal ≥992 / stacked <992) |
| 7 | Post grid (wide + normal cards) | `NEW BlogPostCard` (prop `variant: 'wide' \| 'normal'`), using `NEW CategoryTag` |
| 8 | Pagination | `NEW BlogPagination` |
| 9 | Final CTA | `REUSE FinalCta` (identical) |
| 10 | Footer | `REUSE SiteFooter` (identical) |
| 11 | Cookie banner | `NEW CookieConsent` (global) |

### 1.2 `/blog/<category>` (development, feeding, health, news, pregnancy, sleep; plus `/blog/authors` tab, out of scope)
Same template as `/blog` (`BlogIndexPage` with `category` prop), with these differences:
- no AnnouncementBar
- the active tab is the category
- `<title>` pattern per §0.4
- **content = only that category's featured set** (see §2.7). Health and pregnancy have none, so their grid is empty (0px) with "Page 1 of 1".

### 1.3 Article `/blog/<category>/<slug>`
| # | Section | Tag |
|---|---|---|
| 1 | Header | `REUSE SiteHeader` (no AnnouncementBar) |
| 2 | Back + search row (≥992) / search only (<992) | `NEW ArticleTopBar` (uses `BlogSearch`) |
| 3 | Breadcrumbs | `NEW ArticleBreadcrumbs` |
| 4 | Share buttons (3 placements) | `NEW ShareButtons` (prop `variant: 'top' \| 'toc' \| 'bottom'`) |
| 5 | Title, description, bylines, updated/read time, hero image | `NEW ArticleHeader` (+ `NEW AuthorByline`) |
| 6 | Sticky TOC (≥992) / inline "In this article:" (<992) | `NEW ArticleToc` |
| 7 | Portable-text body | `NEW ArticleBody` with block renderers: `Paragraph`, `H2`, `H3`, `BulletList`, `CitationSup`, `InlineLink`, `PromoUnit`, `EditorNote`, `ArticleImage`, `DownloadableImage` |
| 7a | Promo unit button | `REUSE Button`. **Prop difference:** base bg `#7B63F5` (inline style on the original), active `#5A20E1`, hover **UNVERIFIED**, line-height 28 (inherited from prose), `data-button-id="final-cta"`. The current `Button` spreads `style` over all states, so add a `colors` prop (e.g. `colors={{base:'#7B63F5',hover:'#7B63F5',active:'#5A20E1'}}`). |
| 8 | "N sources cited" accordion | `NEW SourcesAccordion` |
| 9 | Bottom share row | `ShareButtons variant="bottom"` (NEW above) |
| 10 | "You'll also love these posts:" | `NEW RelatedPosts` (renders empty on the original; see §3.9) |
| 11 | Final CTA | `REUSE FinalCta` (identical) |
| 12 | Footer | `REUSE SiteFooter` |
| 13 | Cookie banner | `CookieConsent` |

### 1.4 `/editorial-process`
| Section | Tag |
|---|---|
| AnnouncementBar, SiteHeader | `REUSE` |
| Prose body | `NEW TextPage` (prose section, §4) |
| SiteFooter | `REUSE` (directly after main; no FinalCta) |

### 1.5 `/tos`, `/privacy`, `/cookies`
| Section | Tag |
|---|---|
| AnnouncementBar, SiteHeader, SiteFooter | `REUSE` |
| Policy body | `NEW LegalPage`. Renders **empty** on the original (§5). Suggested: reuse `TextPage` with a placeholder and a link to the Termly policy viewer. |

---

## 2. Blog index template (`/blog`, `/blog?page=N`, `/blog/<category>`)

### 2.1 Page skeleton and heights
- `div.mb-[4rem].flex.flex-col.items-center.gap-[5rem].self-stretch` (mb 64, gap 80) contains two children:
  - `div.flex.w-full.flex-col.items-center.justify-center.gap-8.px-4.md:px-8.lg:px-16.mb-8`: padding-x **64 ≥992 / 32 ≥768 / 16 <768**, mb 32, gap 32. It contains:
    - `div.mt-[5rem].flex.w-full.max-w-[90rem].flex-col.items-center.gap-4.md:gap-[5rem]`: mt 80, max-w 1440, gap **80 ≥768 / 16 <768**. Its children are Hero (§2.2), Search (§2.3), and Tabs + grid.
  - Pagination (§2.6)
- Then FinalCta, then SiteFooter.

| Doc height | 1440 | 768 | 390 |
|---|---|---|---|
| `/blog` page 1 | **4794** | **7655** | **8116** |
| `/blog?page=2` | 4754 | | |
| `/blog/sleep` (3 posts) | 3119 | | |
| `/blog/health` (0 posts) | 1999 | | |

Y positions @1440 on `/blog` (with the 54.4 announcement bar): hero top 214.4, search 438.4, tabs 572.4, featured 665.4, grid 1138.4, pagination 3438.4, FinalCta 3592.4, footer 4300.4.

### 2.2 BlogIndexHero
- Row `div.flex.items-center.justify-between.self-stretch`: 1312x144 @1440.
  - Left: `img` blogmascot.svg **138x136**, `hidden md:flex`, alt "Riley Mascot". Rendered at y +4 (vertically centred).
  - Centre: `div.flex.max-w-[36rem].flex-1.flex-col.items-center.justify-center.gap-10` (max-w 576) → `div.flex.flex-col.items-start.gap-4.self-stretch` (gap 16):
    - `h1` "Riley Articles": Recoleta (`"serif"`) **64px/72px ≥992, 40px/48px <992**, #2e2a42, centred. 576x72 @1440.
    - `h3` "Helpful articles with all the information you need to raise happy, healthy children!": Cadiz Regular **20px/28px** at all widths, #2e2a42, centred. 576x56 @1440, 452x56 @768, 358x84 @390.
  - Right: `img` books.svg **114x136**, `hidden md:flex`, alt "Book icon".
- @768 the mascot and books show (x 32 and x 622); the centre column is 452 wide. @390 both images are hidden and the block is 358x148.

### 2.3 BlogSearch
- Wrapper `div.relative.w-full` → `div.shadow-2xs.mx-auto.w-full.rounded-[5rem].lg:max-w-md` (computed shadow is effectively none). Width **448 ≥992**, full container width below (358 @390). Height **54**.
- Icon: absolute left, `ps-5` (20px), 16x16 magnifier, stroke #5934C5 2px (`/assets/blog/icons/search.svg`).
- Input `type="search" required placeholder="Search blog article..."`:
  - bg white, border 1px #d1d5dc, radius 80, padding 16px 16px 16px 48px
  - Cadiz Regular **14px/20px**, colour #101828
  - Focus: border #5934c5 plus the browser default focus outline. No ring.
- Behaviour (measured), a live type-ahead and not a form submit:
  - Typing fetches `/api/search-articles?q=<term>` (full-text). The URL does not change. Enter does nothing extra. Clearing the input removes the dropdown.
  - Clone: filter `blogPosts.json` by title/excerpt locally.
  - Dropdown `div.absolute.z-20.mt-1.flex.max-h-[320px].w-full.flex-col.overflow-y-scroll.rounded-2xl.bg-white.shadow-xl`:
    - margin-top 4, max-h 320 (scrolls), radius 16, bg white
    - shadow `0 20px 25px -5px #0000001a, 0 8px 10px -6px #0000001a`
    - Motion: framer `opacity 0 → 1`, transform none. Opacity stayed 0 for about 200ms after mount and reached 1 by 266ms. Exact curve **UNVERIFIED**; use a 0.2s fade.
  - Item `a.block.border-b.px-4.py-3` (padding 12px 16px, bottom border 1px #e5e5e5, 448x69). Hover bg is undefined (none).
    - Row 1 `flex flex-row gap-1`: category label `div.rounded.px-1.text-sm` (Cadiz Regular 14/20, radius 4, padding 0 4px, no bg or colour, #0a0a0a), then title `div.truncate` (16/24 #0a0a0a, single-line ellipsis).
    - Row 2 `div.text-sm.text-gray-500`: snippet with "... " ellipses, 14/20 #6a7282. The match is wrapped in `<mark>` (bg #ffff00, colour #000).
  - Empty state: one `div.flex.flex-col.items-center.justify-center.px-4.py-3` "No results found".

### 2.4 BlogCategoryTabs
- `div.mb-8.flex.justify-center` (mb 32) → `nav.w-full` → `ul.flex.items-center.gap-4.overflow-x-auto.border-b.border-gray-200.md:justify-center.whitespace-nowrap`:
  - gap 16, bottom border **1px #e5e7eb**, 61 tall
  - centred ≥768; left-aligned and horizontally scrollable <768 (starts at x 16 @390; total ≈ 860px wide)
- `li.relative.flex.items-center.justify-center.py-2.flex-shrink-0` (padding 8px 0) → `a.px-4.py-2.text-lg.transition-all.duration-300` (padding 8px 16px, 44 tall):
  - **Active**: Cadiz Bold 18/28 #2e2a42, plus `div.absolute.bottom-0.left-0.h-0.5.w-full.bg-brand-500`. That indicator is 2px tall but **transparent** on live, so the only active cue is bold, darker text.
  - **Inactive**: Cadiz Regular 18/28 **#6a7282**.
  - Hover: `hover:text-brand-400` is a no-op. `transition: all 300ms cubic-bezier(.4,0,.2,1)`.
- Tabs in order, with widths @1440:

| Label | href | width |
|---|---|---|
| All | `/blog` | 55.5 |
| Feeding | `/blog/feeding` | 97.4 |
| Pregnancy | `/blog/pregnancy` | 120.1 |
| Sleep | `/blog/sleep` | 77 |
| Health | `/blog/health` | 85.5 |
| Development | `/blog/development` | 140.1 |
| News | `/blog/news` | 77.5 |
| Authors | `/blog/authors` | 97.4 |

  The tab order comes from `/api/get-blog-categories`. Authors is out of scope.

### 2.5 Grid and cards
Grid: `div.grid.grid-cols-1.gap-8` (gap 32) with two children:

**(a) Featured row** `div.col-span-full`:

- **Desktop ≥992**: `div.bg-blogFeature.group.hidden.items-center.justify-between.self-stretch.overflow-hidden.rounded-3xl.bg-white.lg:flex`. White, radius 24, **1312x441** @1440. It contains `a.group.flex.flex-1.items-center.gap-4` (gap 16), which links to the post.
  - Left column `div.flex.flex-1.flex-col.items-start.gap-8.self-stretch.px-[3.75rem].py-[2.5rem]`: 708 wide, padding **40px 60px**, gap 32. Contents:
    1. `div.flex.flex-col.items-start.gap-5` (gap 20) holding:
       - CategoryTag **large** (152.2x40.9, label Cadiz Bold 16/24)
       - `h2` Cadiz **Bold 30px/36px** #2e2a42, mb 8, `transition-all 300ms` (group-hover colour is a no-op). 588x72.
    2. Author row `div.flex.items-center.gap-4`: avatar `img.rounded-full` 48x48, then name `p` Cadiz Bold 16/24 #2e2a42 and title `div` Cadiz Regular 16/24 #2e2a42 (opacity class ignored).
    3. Excerpt `p` Cadiz Regular 16/24 #2e2a42, no clamp.
    4. `div.flex.items-center.gap-4`: "Read more" Cadiz Bold 16/24 **#0a0a0a**, then a 6x11 chevron (stroke #7B63F5, width 1.64; `/assets/blog/icons/read-more-chevron.svg`).
  - Right column `div.flex.w-full.max-w-full.flex-1.flex-col.items-start.self-stretch` → `img.h-48.w-full.flex-1.self-stretch.object-cover.md:h-[400px]`. Rendered **588x441**, object-fit cover (stretches to row height). Source `_next/image w=1200`.
  - On `/blog/sleep` the banner is 412 tall (shorter excerpt).
- **Mobile/tablet <992**: `div.bg-blogFeature.group.flex.flex-col.items-start.gap-8.self-stretch.overflow-hidden.rounded-3xl.bg-white.pb-8.lg:hidden`. Radius 24, pb 32, gap 32. Sizes: 358x717.3 @390, 704x816.8 @768. It contains `a.flex.w-full.flex-col.items-center.gap-4` (gap 16):
  - Image wrapper `div.flex.max-h-[28rem].w-full.flex-col.items-start.self-stretch.overflow-hidden` → `img.w-full.flex-1.self-stretch.object-cover`. Natural aspect, capped at 448: 358x268.5 @390, 704x528 @768.
  - Body `div.flex.flex-col.items-start.gap-6.self-stretch.px-6` (padding 0 24px, gap 24):
    1. CategoryTag large
    2. `div.flex.flex-col.items-start.gap-6` (gap 24) holding:
       - `h2` Cadiz **Bold 24px/32px**
       - author row: avatar 48, name 16/24 Bold, title 16/24 Regular; 72 tall when the title wraps
       - excerpt 16/24
    3. "Read more" row (same as desktop)
- Featured content is fixed per listing, not per page; see §2.7.

**(b) Post grid** `div.grid.grid-cols-1.gap-8.lg:grid-cols-3`:
- Columns: **416 / 416 / 416** @1440 (gap 32); 1 column <992 (704 @768, 358 @390).
- Item 1 is `div.col-span-1.lg:col-span-2`, the **wide card** (864 @1440). Every other item is `div.col-span-1`. So row 1 = wide + 1, then rows of 3. Page 1 has 8 cards: 2 placement cards + 6 posts.
- Card `div.group.flex.h-full.flex-col.items-start.gap-8.self-stretch.overflow-hidden.rounded-3xl.bg-white`: white, radius 24, gap 32, `h-full` (equal heights per row). Card heights @1440: row 1 748, row 2 692 / 684, row 3 684 / 652.
  - `a.flex.w-full.flex-col.gap-8` (gap 32; text colour classes undefined) wraps everything except the author link:
    1. `div.flex.w-full.flex-col.items-start.self-stretch` → `img.h-48.w-full.object-cover.lg:h-[16rem]`: height **256 ≥992 / 192 <992**, full card width, cover. Sources `_next/image` w=828 (wide) / w=640.
    2. Body `div.flex.flex-1.flex-col.items-start.justify-between.gap-5.self-stretch.px-6.pb-8.md:px-10`: padding-x **40 ≥768 / 24 <768**, pb 32, gap 20. Contents:
       - `div.flex.flex-col.items-start.gap-3` (gap 12):
         - meta row `div.flex.items-center.gap-6` (gap 24): date `p` Cadiz Regular 16/24 #2e2a42 ("8 Apr 2025"), then optional read time `p` 16/24 #2e2a42 ("4 min read"). The row stays empty (0 tall) when there is no date. The 12px gap still applies.
         - `h2` Cadiz **Regular** (the semibold class is undefined) **30px/36px for the wide card, 24px/32px for normal cards**, #2e2a42, mb 8, `transition-all 300ms`, hover no-op.
       - Excerpt `p` Cadiz Regular 16/24 #2e2a42, `line-clamp-4` (wide) / `line-clamp-3` (normal).
       - Author `div.flex.flex-col.gap-1` (gap 4):
         - row `div.flex.items-center.gap-3` (gap 12): "By" span 16/24, then the name. On the 2 placement cards the name is `a` → `/blog/author/<slug>` (`transition-colors 200ms`, hover no-op). On regular cards it is a `span`. Both 16/24 #2e2a42.
         - second row: author title span 16/24 #2e2a42 (19.5px box).
       - CategoryTag **small** (40 tall, icon 16x16).
- Hover: no visible change on cards. There is no image zoom (unlike `BlogTeaser`), and the `hover:text-*` classes resolve to nothing.

### 2.6 BlogPagination
- `div.mb-[3rem].flex.items-center.justify-center.gap-4.self-stretch`: mb 48, gap 16, 42 tall, centred. Contents:
  1. Prev `a.flex.items-center.gap-2.rounded-[6.25rem].border.px-4.py-2`: border 1px **#e5e5e5**, radius 100, padding 8px 16px, gap 8, 83.1x42. Holds the 8x11 chevron (`pagination-prev.svg`, stroke #7B63F5) and "Prev" Cadiz Regular 16/24 #0a0a0a.
     - Page 1: `href="#"`, `aria-disabled="true"`, `pointer-events-none opacity-50`.
     - Otherwise: `href="/blog?page=N-1"`. Page 2 links to `/blog?page=1`.
  2. `div.flex.items-center.gap-2` (gap 8): "Page" span, then `button` with the current number (padding 0 4px, bottom border 1px transparent, `transition-colors 200ms`; click behaviour **UNVERIFIED**), then "of 37" span. All Cadiz Regular 16/24 #0a0a0a.
  3. Next: same pill, "Next" then the 7x11 chevron (`pagination-next.svg`), `href="/blog?page=N+1"`. On the last page it is disabled the same way as Prev.
- Navigation is a normal link: a full route change with the scroll reset to top. There is no "load more" or infinite scroll.

### 2.7 Data and pagination logic (from the server payload)
- `/blog` ships **all 221 posts** (`allPosts`) in a fixed order. `blogPosts.json` keeps that order in `order` (0-220).
- **Page size 6.** `totalPages = ceil(221/6) = 37`. Page N shows `allPosts[(N-1)*6 .. N*6]`.
- On **every** `/blog` page the same featured items are prepended:
  - banner: `why-we-built-riley`
  - wide card: `introducing-golden-window`
  - card 2: `welcome-dr-lilly-jay`
  Featured items repeat on every page. `featured.blog` = `hero` / `card` in the JSON.
- Category pages show **only** their configured featured set (banner + up to 2 cards) and "Page 1 of 1", with both Prev and Next disabled. This is a live-site quirk; regular category posts are not listed. `featured.<category>` in the JSON:

| Category | Banner | Cards |
|---|---|---|
| sleep | 1-month-old-sleep-guide | what-is-newborn-day-night-confusion, when-do-babies-start-sleeping-through-the-night |
| development | how-to-play-with-your-newborn | when-do-babies-start-crawling, understanding-baby-growth-charts |
| feeding | night-feedings-when-and-how-to-wean | 6-month-old-feeding-schedule, baby-feeding-schedules |
| news | why-we-built-riley | welcome-dr-lilly-jay, introducing-golden-window |
| health, pregnancy | none (empty grid, 0px tall; doc 1999 @1440) | |

  Decide with the caller whether to reproduce the empty categories faithfully or filter `blogPosts.json` by category.
- Post counts per category: sleep 119, development 47, pregnancy 21, feeding 12, health 11, news 11 (= 221).

### 2.8 Motion (blog index)
| Element | Trigger | Effect | Timing |
|---|---|---|---|
| Category tab | hover | none visible (`transition-all 300ms cubic-bezier(.4,0,.2,1)` declared) | |
| Card / featured title | group hover | none visible (`transition-all 300ms`) | |
| Card author link, page-number button | hover | none visible (`transition-colors 200ms`) | |
| Search dropdown | results arrive | opacity 0 → 1 (framer) | about 0.2s; curve **UNVERIFIED** |

No scroll-triggered animations: computed styles were identical before and after scrolling.

---

## 3. Article template (`/blog/<category>/<slug>`)

### 3.1 Skeleton and widths
- `article.my-[1rem].flex.w-full.justify-center.lg:my-[4rem]`: margin-y **64 ≥992 / 16 <992**. It contains `div.flex.w-full.max-w-[90rem].flex-col.items-center.gap-[7.5rem]` → `div.flex.flex-col.items-center.gap-[2rem].self-stretch.lg:gap-[5rem]` (gap **80 / 32**). Children in order:
  1. TopBar (§3.2)
  2. Content column `div.flex.flex-col.items-center.justify-center.gap-[2.75rem].self-stretch.px-5.lg:gap-[5.5rem].lg:px-0`: gap **88 ≥992 / 44**, padding-x **0 ≥992 / 20 <992**.
  3. FinalCta. It sits inside the same gap-80 column, so it is 80px below the related-posts block.
- Desktop (≥992) content column children:
  - Header block `div.hidden.flex-col.items-center.gap-[4.5rem].self-stretch.lg:flex.lg:max-xl:px-[6.5rem].xl:px-[13rem]`: padding-x **208 ≥1280 / 104 at 992-1279**, gap 72. Content width **1024 @1440**.
  - Body row `div.hidden.items-center.justify-center.self-stretch.lg:flex.lg:max-xl:px-[2.75rem].xl:px-[5.5rem]`: padding-x **88 ≥1280 / 44 at 992-1279**. It contains `div.flex.flex-1.items-start.gap-[5.5rem]` (gap 88) with:
    - TOC aside: **256** wide
    - Prose column `div.prose.flex.w-full.max-w-[1280px].flex-1.flex-col.items-start.justify-center`: **920 @1440** (x 432). At 1280: 1280 − 176 − 256 − 88 = 760.
  - Related posts block (§3.9).
- Mobile/tablet (<992) uses separate `lg:hidden` markup. Order: header block (breadcrumbs, title, hero, description, meta, bylines), then inline TOC + share, then prose `div.prose.flex.w-full.max-w-[991px].flex-col.items-start.justify-center.gap-[2.5rem].self-stretch` (350 @390, 728 @768), then sources, share row, related.

| Doc height | 1440 | 768 | 390 |
|---|---|---|---|
| A1 baby-witching-hour (92 blocks) | **10317** | **12951** | **16959** |
| A2 23-month-old-sleep-schedule | 8615 | | |
| A3 introducing-the-new-riley | 10078 | | |
| A4 maternity-leave-planning | 12451 | | |
| A5 free-baby-tracker-apps | 10651 | | |

### 3.2 ArticleTopBar
- **≥992**: `div.hidden.items-center.justify-between.gap-4.self-stretch.px-[6.25rem].lg:flex`: padding-x 100, 54 tall, y 144 @1440 (header 80 + article margin 64).
  - Left: `a[href="/blog"].flex.items-center.gap-4` (gap 16). Holds the back arrow 18x26 (`/assets/blog/icons/back-arrow.svg`, stroke #2E2A42 width 4.13, round caps) and "Back" span Cadiz Regular **16px/20px** #2e2a42.
  - Right: `div.w-[400px]` holding BlogSearch (400x54).
- **<992**: `div.w-full.items-center.px-5.lg:hidden` (px 20) holds BlogSearch at full width (350x54 @390). There is no Back link. y 96 @390.

### 3.3 Header block, desktop (≥992)
`div.flex.flex-col.items-center.justify-center.gap-8.self-stretch` (gap 32), 1024 wide @1440. Children:
1. Row `div.flex.w-full.items-start.justify-between` with:
   - **ArticleBreadcrumbs** `nav` → `ol.flex.items-center.space-x-3` (12px spacing). Each `li.flex.items-center.gap-3` (gap 12):
     - "Blog" `a[href=/blog]` (`hidden lg:flex`)
     - chevron (lucide chevron-right 16x16, stroke **#99a1af** width 2; `/assets/blog/icons/breadcrumb-chevron.svg`; hidden <992)
     - category `a[href=/blog/<cat>]`
     - chevron
     - current-page pill `span.rounded-full.px-6.py-2`: bg = category colour from §0.2 (sleep #EACDFF), padding 8px 24px, radius full, wraps (604x64 @1440 for a 2-line title)
     - Links and the pill are Cadiz Regular 16/24 #2e2a42. Link hover `hover:text-gray-700` → **#364153**.
   - **ShareButtons variant="top"** (§3.8), right-aligned, 267.6x66.
2. Title block `div.flex.flex-col.items-start.gap-4.self-stretch` (gap 16):
   - `h1` Recoleta **64px/72px**, #2e2a42, left-aligned, full width (1024)
   - description `h3` Cadiz Regular **16px/25.2px** #2e2a42
3. Meta row `div.flex.w-full.items-start.justify-between`:
   - Left `div.flex.flex-1.items-end.gap-4` holds 1 or 2 **AuthorByline** blocks (gap 16): `div.flex.items-center.gap-4.self-stretch` → avatar `img.rounded-full` **82x82** (80.3 tall for non-square sources), then `div.flex.flex-col.items-start.gap-1` (gap 4):
     - label `p` "Written by:" or "Reviewed by:" (Cadiz Regular 16/24 #0a0a0a)
     - name `a` 16/24 #0a0a0a → `/blog/author/<slug>` or `/blog/reviewer/kate-roche` (`hover:underline` works)
     - title `p` 16/24 #0a0a0a, for example "Founder & CEO of Riley, Certified Pediatric Sleep Consultant" or "Director, Riley Clinical Advisory Board"
     - 187/221 posts have the reviewer block (Dr. Kate Roche, M.D.)
   - Right `div.flex.flex-col.items-end.justify-center.gap-2` (gap 8): "Updated: 21 Jul 2025" 16/24 #2e2a42, then optional "10 min read" 16/24 #0a0a0a.
4. Hero `div.flex.items-start` → `div.flex.max-h-[30rem].flex-1.flex-col.items-center.justify-center.overflow-hidden.rounded-2xl`: **1024 x 480 max**, radius 16. Inside, `img.h-auto.self-stretch` has its natural aspect (1024x682.7) and is **vertically centred and clipped**: the image top is 101px above the box. Alt = `mainImage.alt` (may be empty).

The header block ends 72px above the body row.

### 3.4 Header block, mobile/tablet (<992)
`div.flex.flex-col.items-start.gap-[4.5rem].self-stretch.lg:hidden` → `div.flex.flex-col.items-center.justify-center.gap-8.self-stretch` (gap 32). In order:
1. Breadcrumbs (no "Blog" crumb and no first chevron): category link, then chevron, then pill (279.8 wide @390, wraps to 88 tall).
2. `h1.h1-mobile` Recoleta **40px/48px**.
3. `div.flex.flex-col.items-start.gap-8` (gap 32) holding:
   - hero `div.flex.h-[16.5rem].w-full.flex-col.items-start.justify-center.overflow-hidden.rounded-2xl` (**264** tall, radius 16) with `img.h-auto.w-full.self-stretch.object-cover`, natural height (233 @390), vertically centred
   - description 16/25.2
4. `div.flex.items-center.justify-between`: "Updated: …" on the left, "N min read" on the right.
5. Bylines `div.flex.flex-col.items-start.justify-end.gap-4` (gap 16; each byline row 104 tall @390 because the title wraps).

### 3.5 ArticleToc
- **Desktop**: aside `div.sticky.top-[5rem].h-screen.w-[16rem].flex-shrink-0.overflow-y-auto` (sticky top **80**, height 100vh, width 256) → `nav.relative.flex.w-full.flex-col.items-center.justify-start.gap-[2.5rem].lg:sticky.lg:top-5.lg:max-w-[16rem].lg:items-start.lg:border-none.lg:p-0` (sticky top 20 inside, gap 40, no border or padding). Children:
  1. `div.flex.items-start.gap-4.self-stretch.lg:gap-5` (row, gap 20) with:
     - progress track `div.w-1.h-full.bg-[#D9D9D9]` (4px wide, full list height) containing the fill `div.absolute.left-0.top-0.w-full.bg-brand-500.transition-all.duration-300`. The fill height follows scroll progress (0 at top; 167.8px when heading 3 is scrolled into view; 336 = full at mid-page). Its bg is **transparent on live**, so it is invisible. `transition all 300ms cubic-bezier(.4,0,.2,1)`.
     - `ul.flex.flex-1.flex-col.items-start.gap-2` (gap 8) of `li` (transition-all 300ms) → `a[href="#<heading-slug>"].hover:underline`. Cadiz Regular 16/24 #0a0a0a. Items wrap within 232px.
     - One entry per **h2** (`post.headings` level h2). The anchor id is the slugified heading text, e.g. `what-is-witching-hour`. Headings have scroll-margin 0.
     - The active-item class toggles brand-300/brand-600, which are both undefined, so there is no visible active state.
  2. ShareButtons variant="toc".
- **Mobile**: `div.flex.flex-col.items-center.justify-center.gap-[2.5rem].self-stretch.py-8` (py 32) → `nav` with **1px solid #2e2a42 border on all 4 sides**, py 32, gap 40 (350x428 @390). Inside:
  - `div.flex-col.gap-4` (gap 16): `span` "In this article:" Cadiz Regular 16/24 #2e2a42, then the same `ul` (gap 8). No progress track.
  - Share row (copy-link button 121.5x42 single line).
- Clicking a TOC link jumps to the anchor with no smooth scroll (CSS `scroll-behavior` default).

### 3.6 ArticleBody: block renderers (prose column)
The container is `div.mb-8.flex.flex-col` (mb 32) inside the prose column. Base text is Cadiz Regular 16px/28px.

| Block (Sanity) | Element / classes | Desktop ≥992 | Mobile <992 |
|---|---|---|---|
| `block` normal | `p.paragraph.text-text-primary.my-0.text-opacity-90.lg:my-4` | 16/28 #2e2a42, margin **16px 0** | margin **20px 0** (first p 0 0 20) |
| `block` h2 | `h2.h2-small-mobile.font-sansBold.text-text-primary.lg:h2-small.my-0.lg:mb-8.lg:mt-4` (`id` = slug) | Cadiz **Bold 24px/32px**, weight 700, #2e2a42, margin **16px 0 32px** | same font, margin **48px 0 24px** |
| `block` h3 | `h3.h3-small-mobile.font-sansBold … lg:mb-4 lg:mt-8` | Cadiz **Bold 20px/32px**, weight 600, margin **32px 0 16px** | margin **32px 0 12px** (0 0 12 directly after an h2) |
| `block` h1 (1 post: 3-month-sleep-regression) | not measured | **UNVERIFIED** | |
| bullet list (`listItem: bullet`, level 1) | `ul.my-0.list-disc.pl-5.lg:mt-2` → `li.font-sansRegular.mb-1` | ul: padding-left **20**, margin **8px 0 20px**. li: disc outside, **#364153**, 16/28, padding-left 6, margin 8px 0 4px | ul margin 20px 0 (0 0 20 after a heading) |
| bullet level 2 | nested `ul` (same classes) inside the `li` | margin **8px 0 12px**, li indented +26 (x 478 vs 452), disc marker | same |
| `strong` mark | `strong.font-sansBold.text-text-primary` | Cadiz Bold, weight 600, #2e2a42 | |
| `em` mark | `em.italic` | synthetic italic of Cadiz Regular | |
| `link` markDef | `a.text-brand-500.hover:underline` (prose link) | **#101828**, weight 500, underline (prose default), absolute `https://rileyapp.com/blog/...` hrefs. When it wraps `strong` the text shows #2e2a42 bold. | |
| `citation` markDef | `sup` (relative) → `a.text-brand-500.hover:underline[href="#source-N"]` text `[ N ]` | 12px, line-height 0, weight 500, #101828, underline. About 13-16px wide. | |
| `image` | `div.my-8` → `img.rounded-lg` | wrapper margin 32px 0 (first: 0 0 32). img **800** wide (next/image width 800, natural ratio; 800x515.6), radius **10px**, margin 32px 0, left-aligned in the 920 column | max-width 100% |
| `downloadableImage` | `div.relative.mb-4.max-w-full` → `div.flex.w-full.flex-col` → `img.h-auto.w-full` + `button.group.absolute.right-2.top-2.rounded-full.bg-white.p-2.shadow-md.transition-all.duration-300.lg:p-4` | img full width (920), margin 32px 0, wrapper mb 16. Button at top 8 / right 8, **60x60** (p 16) on ≥992, white, shadow-md, holding lucide download 28x28 stroke #2e2a42 (`/assets/blog/icons/download.svg`). Hover: `hover:bg-brand-400` is a no-op while the icon turns white (`group-hover:text-white`), so on live the icon disappears on hover. `transition all 300ms`. | p 8 → 44x44 |
| `editorNote` | `div.my-4.flex.flex-col.items-start.gap-6.self-stretch.rounded-xl.bg-brand-100.p-8.lg:flex-row.lg:p-[3rem]` | margin 16px 0, padding **48** (32 <992), row on ≥992 with gap 24, radius 14, **bg transparent on live**. Left `img` editor-mascot.svg **71x64** (margin 32px 0). Right `div.flex.flex-1.flex-col.gap-4`: `h3` "Editor's Note" Cadiz Regular 20/32 weight 600, margin 32 0 12, plus a nested `.prose` holding paragraphs (16/28) | column layout |
| `promoUnit` | see §3.7 | | |

Notes:
- Paragraph and link colours inside the prose: the prose body var is #364153, but `p` elements carry #2e2a42.
- No tables, blockquotes, callout boxes or ordered lists exist in any of the 221 posts (portable-text type tally over all posts: block normal/h1/h2/h3, bullet lvl 1-2, image ×1 post, downloadableImage ×1, editorNote ×5, promoUnit ×99, marks strong/em, markDefs link/internalLink/citation).
- Per the content policy, the clone renders placeholder paragraphs plus a "Read the original" link (`post.url`), while keeping the heading list for the TOC where wanted.

### 3.7 PromoUnit (99 posts; inserted after the first paragraph on A1/A2)
- Outer `div.relative.mx-auto.mb-[4rem].flex.w-full.max-w-[90rem].items-center.justify-center.self-stretch.px-5.xl:mt-[5rem].xl:px-[6.25rem]`: margin-top **80 ≥1280** (0 below), mb 64, padding-x **100 ≥1280 / 20**.
- Card `div.flex.w-full.flex-1.flex-col.items-center.gap-6.rounded-3xl.bg-greenGradient.px-5.xl:px-0.xl:gap-4.py-8`:
  - bg `linear-gradient(253.62deg, #FFDF78 5.6%, #D2F2D2 72.1%)`, radius 24, padding **32px 0** ≥1280 / 32px 20px, gap 16 (24 below)
  - **720x272 @1440**, 310x392 @390
- Inner `div.mx-auto.flex.max-w-[638px].flex-col.items-center.gap-8.xl:gap-6` (max-w 638, gap 24 ≥1280 / 32) holds:
  - `p.text-center`: 16/28 **#364153**, margin 20px 0. Per-post copy (content; use a placeholder like "Download Riley now using code RILEYBLOG20 to get 20% off.").
  - Button "Get Started", full width **638x60**, Cadiz Bold 16/28, base bg **#7B63F5**, mousedown **#5A20E1**, hover **UNVERIFIED**. Click target **UNVERIFIED** (no href in DOM).

### 3.8 ShareButtons
Group `div.flex.items-center.gap-2.space-x-2`: 8px gap plus 8px margin-right per item, so items are 16px apart.

- **Copy link** button: `button.flex.items-center.space-x-2.rounded-full.border.border-gray-200.bg-white.px-4.py-2.font-sansRegular.hover:bg-gray-300`
  - border 1px #e5e7eb, radius full, padding 8px 16px, Cadiz Regular 16/24 #2e2a42
  - hover bg **#d1d5dc** (instant; no transition)
  - Icon `copy-link.svg` 21x23 (stroke #2E2A42 1.52, margin-right 8)
  - Sizes: top variant 116.6x66 (label wraps to 2 lines); bottom variant 131.5x46 (one line)
  - TOC variant: `px-3 py-2 gap-1.5` (padding 8px 12px, gap 6), 105x66 desktop / 121.5x42 mobile
- **On click**: the icon is replaced by a lucide check 16x16 (`check.svg`) and the label by "Copied!". It reverts to "Copy link" within 2.8s (exact timeout **UNVERIFIED**; use 2000ms). No toast.
- **Social** buttons `button.hover:bg-opacity-80` (the hover is a no-op), each a 34x34 circle, fill #2E2A42, white glyph:
  - Facebook `share-facebook.svg`
  - X `share-x.svg`
  - Instagram `share-instagram.svg` (35x34)
  - Click behaviour **UNVERIFIED** (buttons, no href; likely share-intent popups).
- Placements:
  - `top`: header, right of breadcrumbs
  - `toc`: in the sticky aside / mobile TOC
  - `bottom`: `div.flex.items-center.justify-between.self-stretch.border-y.py-8`. Border-y **1px solid #2e2a42** (4 sides on mobile via `border-1`), py 32, 920x134 @1440. Contents: `p` "Share this article:" Cadiz Regular 16/28 #2e2a42 (margin 20px 0), then the group. At 640-767 it stacks (`sm:max-md:flex-col sm:max-md:gap-8`).

### 3.9 SourcesAccordion and RelatedPosts
- **SourcesAccordion** `div.mb-10.flex.w-full.flex-col.items-center.justify-center` (mb 40) → `div.flex.w-full.flex-col.items-start.justify-center.gap-2.self-stretch.rounded-2xl.bg-white.px-6.py-10`: white, radius 16, padding **40px 24px**, gap 8, 920x108 collapsed.
  - Header `div.flex.w-full.cursor-pointer.items-center.justify-between.gap-5`: `h5` "`{n}  sources cited`" (two spaces in the DOM; Cadiz Regular 16/28 #2e2a42, padding 0 4px), then a 24x24 icon box. Collapsed shows `sources-plus.svg` (24x25, fill #2E2A42). Expanded shows `sources-minus.svg` (18x3 stroke).
  - Collapsed: the sources sit in an `sr-only` div (1x1, kept for the `#source-N` anchors).
  - Expanded: `div.mt-6.flex.w-full.flex-col.gap-8` (mt 24, gap 32) of `div#source-N.flex.w-full.flex-col` → `p.text-large.my-0`, Cadiz Regular 16/28 #2e2a42, holding:
    - `span.mr-2.font-sansBold` "N." (margin-right 8)
    - "Author (Year). Title. "
    - `a[target=_blank][rel="noopener noreferrer"].hover:underline`: full URL, #101828 underline
  - Expanded height 848 for 6 sources. Toggle is **instant** (no height transition).
- **RelatedPosts**: wrapper `div.w-full.items-center.justify-center.lg:max-2xl:px-[3rem].2xl:px-[6.25rem]` (padding-x **100 ≥1440 / 48 at 992-1439 / 0**) → `div.flex.flex-col.items-center.justify-center.gap-[2.5rem].sm:px-5` (px 20 ≥640) → `div.flex.flex-col.items-start.gap-[3.75rem]` (gap 60). Contents:
  1. Header row `div.flex.w-full.flex-col.items-center.justify-center.gap-6.lg:flex-row` (gap 24; column and centred <992):
     - `img` 3dglasses.svg rendered **112x63.1** (natural 94x53)
     - `div.flex.flex-1.flex-col.items-start.gap-3` holding `h3.h3-small.font-sansBold` "You'll also love these posts:" (Cadiz Bold 16/24 #2e2a42) and an empty `p` (16/24, 0 tall)
  2. Carousel `div.w-full.overflow-hidden` → `div.flex.gap-8.overflow-x-auto.scroll-smooth` (gap 32). **Renders 0px tall / empty on the live site** at every width, even after a 12s wait; no related-posts request was observed. For the clone, either reproduce it as empty or (suggested) render 3-4 `BlogPostCard variant="normal"` from the same subcategory in a horizontal scroller with 32 gap, and flag it as an enhancement.
  3. `div.flex.w-full.items-center.justify-center.gap-6` → `button.ml-2.rounded-full.border.px-4.py-2.font-sansBold` "See All >" (98.4x42, border 1px #e5e5e5, Cadiz Bold 16/24 #0a0a0a, margin-left 8). No href; suggest linking to `/blog/<category>`.
  - A second, identical, empty wrapper follows (author's other posts; 0 tall).

### 3.10 Motion (article)
| Element | Trigger | Effect | Timing |
|---|---|---|---|
| Desktop TOC aside | scroll | CSS `position: sticky; top: 80px` (nav inside: sticky top 20) | |
| TOC progress fill | scroll | height = scroll progress through the article | `transition: all 300ms cubic-bezier(.4,0,.2,1)`; invisible (transparent) on live |
| Header | scroll >54px | becomes fixed with shadow and blur (same as homepage M2) | 300ms |
| Copy link | click | swaps to check + "Copied!", reverts | ≤2.8s |
| Copy link | hover | bg white → #d1d5dc | instant |
| Sources accordion | click | expand / collapse, icon plus ↔ minus | instant |
| Promo button | mousedown | bg #7B63F5 → #5A20E1 | 300ms all |
| Downloadable image button | hover | icon turns white | 300ms all |

No IntersectionObserver reveals, and `document.getAnimations()` returned none.

---

## 4. TextPage: `/editorial-process`

- After the header: `main` → `section.prose.prose-md.text-text-primary.mx-auto.mt-8.max-w-[90rem]`: margin-top 32, max-w 1440, **no horizontal padding**. At 1440 and at 390 the text starts at x = 0 and spans the full viewport width (an original quirk). Suggestion: keep it faithful; optionally add `px-5 lg:px-16` and note the divergence.
- The prose has no FinalCta; the footer follows the section directly.
- Doc height **2192 @1440**, **3701 @390**. Section 1440x1532 @1440 (y 166.4 → 1698.4).
- Typography (all children wrap text in `span`s from the Storyblok rich-text):

| Element | Font | Colour | Margin |
|---|---|---|---|
| h2 (1×) "Riley's Editorial Process" | Cadiz Regular face, **24px/32px**, weight 800 (strong) | #101828 | 0 0 24px |
| intro / closing p | 16/28 | #2e2a42 | 0 0 20px / 20px 0 0 |
| h3 (6×) | 20px/32px, weight 700 | #101828 | 32px 0 12px |
| ul | | | padding-left 26, margin 0 0 20px |
| li | 16/28 | | padding-left 6, margin 8px 0 |
| li > p | | | 20px 0 (collapses) |
| li strong lead-in ("Topic Selection:") | weight 600 | #101828 | |
| link ("our support form" → `https://rileyapp.com/support`, wrapped in `u`) | weight 500, underline | #101828 | |

  Marker colour is the prose default bullets colour (**UNVERIFIED**).
- Structure (headings only):
  - h2 "Riley's Editorial Process"
  - intro p
  - h3 "Content Development" (3 bullets)
  - h3 "Review and Editing" (3)
  - h3 "Clinical Advisory Board Review" (3)
  - h3 "Final Approval and Publication" (2)
  - h3 "Ongoing Maintenance" (2)
  - h3 "Editorial Standards" (7 plain bullets)
  - closing p with the support link
- Bullets 1-13 are `**Label:** sentence`; the Editorial Standards bullets are plain sentences. Render placeholders per the content policy.

## 5. LegalPage: `/tos`, `/privacy`, `/cookies`

- Storyblok stories "Terms of Service", "Privacy Policy" and "Cookie Policy" each hold a single `termly_embed` block. It renders `<main><div name="termly-embed" data-id="<policyUUID>"></div></main>` and tries to load `https://app.termly.io/embed-policy.min.js`.
- **That script is blocked by the site's own Content-Security-Policy** (console: "violates the following Content Security Policy directive: script-src …"). So on the live site **`main` is empty (0px)**: the page is AnnouncementBar + SiteHeader + empty main + SiteFooter (+ cookie banner). Doc height = viewport (900 @1440, 844 @390; body 628 / 793.4). This was confirmed in both the isolated browser and the shared MCP browser.
- Policy UUIDs for a link-out:

| Route | Policy UUID |
|---|---|
| tos | `1b687b5a-20d7-48f3-be50-cae504edce40` |
| privacy | `8c6a0cc4-5004-4ad9-a563-ee70e8d1d3a6` |
| cookies | `eb7f04dc-b468-448d-8d88-24933fb4f3cb` |

  Viewer URL: `https://app.termly.io/policy-viewer/policy.html?policyUUID=<uuid>` (HTTP 200).
- Suggested clone: `LegalPage` = `TextPage` shell (mt 32) with an h2 (policy name, 24/32 weight 800 #101828), one placeholder paragraph and a link to the Termly viewer. Termly's own policy styling was not measured (it is cross-origin and not rendered on the original).

---

## 6. Assets

All paths are under `/Users/riyaghosh/V3/rileyapp/public`.

| Path | What | Format / size |
|---|---|---|
| `/assets/blog/<slug>.jpg\|png` ×221 | card / OG thumbnail for every post | Sanity `?w=800` transform of `mainImage` (original format: 213 JPEG, 8 PNG); 10 MB total. Filenames are the slug lower-cased with `'` and `:` stripped (3 posts); use `image` from the JSON. |
| `/assets/blog/authors/{amanda-deluca,sam-fore,girish-gupta,kate-roche}.png` | author / reviewer avatars | PNG 192w (rendered 48 on cards, 82 on articles) |
| `/assets/blog/icons/blogmascot.svg` | index hero left | 138x136 |
| `/assets/blog/icons/books.svg` | index hero right | 114x136 |
| `/assets/blog/icons/{moon,bowl,duck,lightbulb,first-aid,octopus}.svg` | category tag icons | 28x28 (bowl and lightbulb 28x29, first-aid 28x25) |
| `/assets/blog/icons/3dglasses.svg` | related-posts header | 94x53 (rendered 112x63) |
| `/assets/blog/icons/editor-mascot.svg` | Editor's Note | 71x64 |
| `/assets/blog/icons/search.svg` | search icon | 20 viewBox, stroke #5934C5 |
| `/assets/blog/icons/read-more-chevron.svg`, `pagination-prev.svg`, `pagination-next.svg` | chevrons | 6x11 / 8x11 / 7x11, stroke #7B63F5 |
| `/assets/blog/icons/back-arrow.svg` | article Back | 18x26 |
| `/assets/blog/icons/breadcrumb-chevron.svg` | breadcrumbs | lucide chevron-right (currentColor → #99a1af) |
| `/assets/blog/icons/copy-link.svg`, `check.svg` | Copy link / Copied! | 21x23 / 16x16 |
| `/assets/blog/icons/share-facebook.svg`, `share-x.svg`, `share-instagram.svg` | social buttons | 34x34, 34x34, 35x34 |
| `/assets/blog/icons/sources-plus.svg`, `sources-minus.svg` | sources toggle | 24x25 / 18x3 |
| `/assets/blog/icons/download.svg` | downloadable image | lucide download 28 |

Reused existing assets: `/assets/background-clouds(1).svg` and `/assets/mascots.svg` (FinalCta), fonts.

Not downloaded (content images): in-article images (A3 ×3, A5 ×1) and full-resolution heroes. The article hero can use the 800w thumbnail (upscaled to 1024) or the `imageSource` Sanity URL with `?w=1200`.

## 7. Data: `src/data/blogPosts.json`

221 objects in the live `allPosts` order. Fields:

| Field | Notes |
|---|---|
| `order` | position in `allPosts` |
| `slug` | |
| `category` | slug |
| `categoryTitle` | |
| `subcategory` | tag label |
| `url` | original article URL |
| `title` | |
| `excerpt` | `description`; it is what the card shows, clamped 3/4 lines |
| `date` | = `updatedAt`; what the cards show |
| `publishedAt`, `updatedAt` | ISO |
| `author`, `authorTitle`, `authorSlug`, `authorImage` | |
| `reviewer`, `reviewerTitle`, `reviewerSlug`, `reviewerImage` | null when there is no reviewer |
| `readTime` | minutes; null on 169 posts |
| `image` | local path |
| `imageAlt` | |
| `imageSource` | Sanity original |
| `seoTitle` | full `<title>` |
| `featured` | e.g. `{ "blog": "hero" }`, `{ "sleep": "card" }`, or null |

Sitemap: 230 `/blog/...` URLs + `/blog` = 231. These are 221 articles, 6 category pages and 3 author pages (`/blog/author/{amanda-deluca,sam-fore,girish-gupta}`).

## 8. Gaps / UNVERIFIED

- **Related posts carousel** renders empty on the live site, so card design and behaviour inside it are unknown.
- **Legal pages** have no content on live (Termly blocked by CSP). Termly layout was not measured.
- Promo `Button` hover colour and click target; social share button click actions; Copy-link revert timeout (≤2.8s); pagination page-number `button` click behaviour.
- Search dropdown fade easing and duration (about 0.2s observed).
- `block:h1` style inside an article body (1 post) was not measured.
- September month abbreviation in dates.
- Author pages (`/blog/author/<slug>`, `/blog/authors`) and the reviewer page (`/blog/reviewer/kate-roche`) are out of scope and were not measured.
- Raw measurement dumps (JSON) are in the recon scratchpad and were not copied into the project.
