# Riley (rileyapp.com) clone — information architecture

Source: https://rileyapp.com/ (live original) · local clone at /src
Status: **measured: all 8 templates specced, built and modelled in design-repo 2.0.0; author/reviewer pages are linked but not built (served by the 404 template)** · production approved: **false**
248 routes · 8 templates · 38 unique sections

> Generated from `ia.json` by `build.mjs`. Edit the JSON, not this file.

## Shape of the site

The largest 3 templates (Blog article, 404 (dead landing slugs + unbuilt links), Blog category) account for 241 of 248 routes (97%). The remaining 7 routes span 5 templates.

| template | routes | share |
|---|---:|---:|
| Blog article | 221 | 89% |
| 404 (dead landing slugs + unbuilt links) | 14 | 6% |
| Blog category | 6 | 2% |
| Legal policy | 3 | 1% |
| Homepage | 1 | 0% |
| Pricing | 1 | 0% |
| Blog index | 1 | 0% |
| Editorial process | 1 | 0% |

## Page chrome

**21 routes carry chrome = `full`** — Homepage, Pricing, 404 (dead landing slugs + unbuilt links), Blog index, Editorial process, Legal policy.

**227 routes carry chrome = `no-announcement-bar`** — Blog category, Blog article.

## Sections by reuse

How widely a section is shared determines whether it belongs in a shared
component library or stays local to its page.

| section | category | templates | routes | implementation | scope |
|---|---|---:|---:|---|---|
| `chrome.site-header` | CHROME | 8 | 248 | `src/components/upper/SiteHeader.jsx` | All 248 mapped routes. |
| `chrome.site-footer` | CHROME | 8 | 248 | `src/components/SiteFooter.jsx` | All 248 mapped routes. |
| `chrome.cookie-consent` | CHROME | 8 | 248 | `src/components/blog/CookieConsent.jsx (mounted in src/App.jsx)` | Every one of the 248 mapped routes (mounted once, globally). |
| `conversion.final-cta` | CONVERSION | 5 | 230 | `src/components/FinalCta.jsx` | 230 routes: homepage, pricing, the blog index, every category page and every article, directly above the footer. |
| `article.top-bar` | ARTICLE | 1 | 221 | `src/components/article/ArticleTopBar.jsx` | All 221 articles. |
| `article.breadcrumbs` | ARTICLE | 1 | 221 | `src/components/article/ArticleBreadcrumbs.jsx` | All 221 articles. |
| `article.header` | ARTICLE | 1 | 221 | `src/components/article/ArticleHeader.jsx (+ AuthorByline.jsx, ShareButtons.jsx)` | All 221 articles. |
| `article.toc` | ARTICLE | 1 | 221 | `src/components/article/ArticleToc.jsx` | All 221 articles. |
| `article.sources` | ARTICLE | 1 | 221 | `src/components/article/SourcesAccordion.jsx` | All 221 articles. |
| `article.share-row` | ARTICLE | 1 | 221 | `src/components/article/ShareButtons.jsx (variant bottom)` | All 221 articles. |
| `article.related-posts` | ARTICLE | 1 | 221 | `src/components/article/RelatedPosts.jsx` | All 221 articles. |
| `article.intro` | ARTICLE | 1 | 221 | `src/components/article/ArticleBody.jsx (+ PromoUnit.jsx)` | All 221 articles. |
| `article.chapter` | ARTICLE | 1 | 221 | `src/components/article/ArticleBody.jsx (+ EditorNote, ArticleImage, DownloadableImage)` | All 221 articles (repeatable). |
| `chrome.announcement-bar` | CHROME | 6 | 21 | `src/components/AnnouncementBar.jsx` | 21 routes: homepage, pricing, every not-found-template route, the blog index, editorial process and each legal page; absent on category and article pages. |
| `error.not-found` | ERROR | 1 | 14 | `src/pages/NotFound.jsx` | 14 routes: the dead sitemap slugs and the linked-but-unbuilt paths (author/reviewer pages, /support), plus any unknown path via the router fallback. |
| `blog.index-hero` | BLOG | 2 | 7 | `src/components/blog/BlogIndexHero.jsx` | Blog index and every category page (7 routes). |
| `blog.search` | BLOG | 2 | 7 | `src/components/blog/BlogSearch.jsx` | Blog index and every category page (7 routes); articles embed the same component inside article.top-bar. |
| `blog.category-tabs` | BLOG | 2 | 7 | `src/components/blog/BlogCategoryTabs.jsx` | Blog index and every category page (7 routes). |
| `blog.featured-banner` | BLOG | 2 | 7 | `src/components/blog/BlogFeaturedCard.jsx` | Blog index and every category page (7 routes); empty on health and pregnancy, which have no featured posts. |
| `blog.post-grid` | BLOG | 2 | 7 | `src/components/blog/BlogPostCard.jsx (+ CategoryTag.jsx)` | Blog index and every category page (7 routes). |
| `blog.pagination` | BLOG | 2 | 7 | `src/components/blog/BlogPagination.jsx` | Blog index and every category page (7 routes); category pages always show a single page. |
| `legal.policy-embed` | LEGAL | 1 | 3 | `src/pages/LegalPage.jsx` | The 3 legal routes (/tos, /privacy, /cookies). |
| `proof.testimonial-carousel` | PROOF | 2 | 2 | `src/components/Testimonials.jsx` | Homepage and pricing (2 routes). |
| `conversion.comparison-table` | CONVERSION | 2 | 2 | `src/components/lower/ComparisonTable.jsx (inside GradientBand.jsx)` | Homepage and pricing (2 routes), inside the gradient band. |
| `support.faq-clouds` | SUPPORT | 2 | 2 | `src/components/FaqClouds.jsx` | Homepage and pricing (2 routes). |
| `hero.home-parallax` | HERO | 1 | 1 | `src/components/Hero.jsx (+ upper/HeroParallaxClouds.jsx)` | Homepage only (1 route). |
| `proof.press-marquee` | PROOF | 1 | 1 | `src/components/Hero.jsx > Marquee (upper/Marquee.jsx)` | Homepage only (1 route). |
| `proof.family-marquee` | PROOF | 1 | 1 | `src/components/PersonalizationMarquee.jsx` | Homepage only (1 route). |
| `product.superpowers-grid` | PRODUCT | 1 | 1 | `src/components/Superpowers.jsx (+ upper/SuperpowerModal.jsx)` | Homepage only (1 route). |
| `product.chat-featurette` | PRODUCT | 1 | 1 | `src/components/Featurette.jsx (+ upper/RiveChat.jsx, shared/useEmblaLoop.js)` | Homepage only (1 route). |
| `proof.clinical-board` | PROOF | 1 | 1 | `src/components/ClinicalBoard.jsx` | Homepage only (1 route). |
| `product.how-it-works` | PRODUCT | 1 | 1 | `src/components/HowRileyWorks.jsx` | Homepage only (1 route). |
| `product.feature-cards` | PRODUCT | 1 | 1 | `src/components/lower/FeatureCards.jsx (inside GradientBand.jsx)` | Homepage only (1 route); the pricing page renders the gradient band without it. |
| `content.blog-teaser` | CONTENT | 1 | 1 | `src/components/BlogTeaser.jsx` | Homepage only (1 route). |
| `hero.pricing-plans` | HERO | 1 | 1 | `src/components/pricing/PricingHero.jsx (+ PlanCard.jsx, upper/HeroParallaxClouds.jsx)` | Pricing only (1 route). |
| `text.header` | TEXT | 1 | 1 | `src/pages/TextPage.jsx` | Editorial process only (1 route). |
| `text.chapter` | TEXT | 1 | 1 | `src/pages/TextPage.jsx` | Editorial process only (1 route; one per level-three heading). |
| `text.closing` | TEXT | 1 | 1 | `src/pages/TextPage.jsx` | Editorial process only (1 route). |

**14 shared sections** appear in more than one template and belong in a component library.

**24 single-use sections** appear in exactly one template. Building these
as "reusable" components up front would be speculative — keep them page-local
until a second caller actually appears.

## Templates

### Homepage — `template.home`

1 route · `/` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.announcement-bar` | shared ×6 |
| 2 | CHROME | `chrome.site-header` | shared ×8 |
| 3 | HERO | `hero.home-parallax` | page-local |
| 4 | PROOF | `proof.press-marquee` | page-local |
| 5 | PROOF | `proof.family-marquee` | page-local |
| 6 | PRODUCT | `product.superpowers-grid` | page-local |
| 7 | PRODUCT | `product.chat-featurette` | page-local |
| 8 | PROOF | `proof.clinical-board` | page-local |
| 9 | PRODUCT | `product.how-it-works` | page-local |
| 10 | PROOF | `proof.testimonial-carousel` | shared ×2 |
| 11 | PRODUCT | `product.feature-cards` | page-local |
| 12 | CONVERSION | `conversion.comparison-table` | shared ×2 |
| 13 | SUPPORT | `support.faq-clouds` | shared ×2 |
| 14 | CONTENT | `content.blog-teaser` | page-local |
| 15 | CONVERSION | `conversion.final-cta` | shared ×5 |
| 16 | CHROME | `chrome.site-footer` | shared ×8 |
| 17 | CHROME | `chrome.cookie-consent` | shared ×8 |

### Pricing — `template.pricing`

1 route · `/pricing` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.announcement-bar` | shared ×6 |
| 2 | CHROME | `chrome.site-header` | shared ×8 |
| 3 | HERO | `hero.pricing-plans` | page-local |
| 4 | PROOF | `proof.testimonial-carousel` | shared ×2 |
| 5 | CONVERSION | `conversion.comparison-table` | shared ×2 |
| 6 | SUPPORT | `support.faq-clouds` | shared ×2 |
| 7 | CONVERSION | `conversion.final-cta` | shared ×5 |
| 8 | CHROME | `chrome.site-footer` | shared ×8 |
| 9 | CHROME | `chrome.cookie-consent` | shared ×8 |

### 404 (dead landing slugs + unbuilt links) — `template.not-found`

14 routes · `/baby-tracker`, `/sleep-tracker`, `/sleep-training`, `/sleep-regression`, `/all-in-one`, `/your-babys-sleep-simplified`, `/product-hunt`, `/give-the-gift`, `/blog/authors`, `/blog/author/amanda-deluca`, `/blog/author/sam-fore`, `/blog/author/girish-gupta`, `/blog/reviewer/kate-roche`, `/support` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.announcement-bar` | shared ×6 |
| 2 | CHROME | `chrome.site-header` | shared ×8 |
| 3 | ERROR | `error.not-found` | page-local |
| 4 | CHROME | `chrome.site-footer` | shared ×8 |
| 5 | CHROME | `chrome.cookie-consent` | shared ×8 |

### Blog index — `template.blog-index`

1 route · `/blog` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.announcement-bar` | shared ×6 |
| 2 | CHROME | `chrome.site-header` | shared ×8 |
| 3 | BLOG | `blog.index-hero` | shared ×2 |
| 4 | BLOG | `blog.search` | shared ×2 |
| 5 | BLOG | `blog.category-tabs` | shared ×2 |
| 6 | BLOG | `blog.featured-banner` | shared ×2 |
| 7 | BLOG | `blog.post-grid` | shared ×2 |
| 8 | BLOG | `blog.pagination` | shared ×2 |
| 9 | CONVERSION | `conversion.final-cta` | shared ×5 |
| 10 | CHROME | `chrome.site-footer` | shared ×8 |
| 11 | CHROME | `chrome.cookie-consent` | shared ×8 |

### Blog category — `template.blog-category`

6 routes · `/blog/development`, `/blog/feeding`, `/blog/health`, `/blog/news`, `/blog/pregnancy`, `/blog/sleep` · chrome: **no-announcement-bar**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.site-header` | shared ×8 |
| 2 | BLOG | `blog.index-hero` | shared ×2 |
| 3 | BLOG | `blog.search` | shared ×2 |
| 4 | BLOG | `blog.category-tabs` | shared ×2 |
| 5 | BLOG | `blog.featured-banner` | shared ×2 |
| 6 | BLOG | `blog.post-grid` | shared ×2 |
| 7 | BLOG | `blog.pagination` | shared ×2 |
| 8 | CONVERSION | `conversion.final-cta` | shared ×5 |
| 9 | CHROME | `chrome.site-footer` | shared ×8 |
| 10 | CHROME | `chrome.cookie-consent` | shared ×8 |

### Blog article — `template.blog-article`

221 routes · `/blog/{category}/{slug}` · chrome: **no-announcement-bar**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.site-header` | shared ×8 |
| 2 | ARTICLE | `article.top-bar` | page-local |
| 3 | ARTICLE | `article.breadcrumbs` | page-local |
| 4 | ARTICLE | `article.header` | page-local |
| 5 | ARTICLE | `article.toc` | page-local |
| 6 | ARTICLE | `article.intro` | page-local |
| 7 | ARTICLE | `article.chapter` | page-local |
| 8 | ARTICLE | `article.sources` | page-local |
| 9 | ARTICLE | `article.share-row` | page-local |
| 10 | ARTICLE | `article.related-posts` | page-local |
| 11 | CONVERSION | `conversion.final-cta` | shared ×5 |
| 12 | CHROME | `chrome.site-footer` | shared ×8 |
| 13 | CHROME | `chrome.cookie-consent` | shared ×8 |

### Editorial process — `template.editorial`

1 route · `/editorial-process` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.announcement-bar` | shared ×6 |
| 2 | CHROME | `chrome.site-header` | shared ×8 |
| 3 | TEXT | `text.header` | page-local |
| 4 | TEXT | `text.chapter` | page-local |
| 5 | TEXT | `text.closing` | page-local |
| 6 | CHROME | `chrome.site-footer` | shared ×8 |
| 7 | CHROME | `chrome.cookie-consent` | shared ×8 |

### Legal policy — `template.legal`

3 routes · `/tos`, `/privacy`, `/cookies` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | CHROME | `chrome.announcement-bar` | shared ×6 |
| 2 | CHROME | `chrome.site-header` | shared ×8 |
| 3 | LEGAL | `legal.policy-embed` | page-local |
| 4 | CHROME | `chrome.site-footer` | shared ×8 |
| 5 | CHROME | `chrome.cookie-consent` | shared ×8 |

## Section reference

### CHROME

_Site-wide frame: announcement bar, header, footer and cookie banner._

**`chrome.announcement-bar`** — Lilac strip above the header with a one-line announcement and link; hidden below 992px.

· 21 routes: homepage, pricing, every not-found-template route, the blog index, editorial process and each legal page; absent on category and article pages. · appears on 21 routes · implemented by `src/components/AnnouncementBar.jsx`

**`chrome.site-header`** — Logo, primary nav links, 'What's New?' and the app CTA; becomes fixed with blur after 54px of scroll; hamburger with slide-up menu below 992px.

· All 248 mapped routes. · appears on 248 routes · implemented by `src/components/upper/SiteHeader.jsx`

**`chrome.site-footer`** — Footer with logo, link columns, newsletter sign-up, app-store badge and copyright line.

· All 248 mapped routes. · appears on 248 routes · implemented by `src/components/SiteFooter.jsx`

**`chrome.cookie-consent`** — Fixed bottom-right translucent cookie notice ('Learn more' → /privacy) with an OK button; hides for a year once accepted.

· Every one of the 248 mapped routes (mounted once, globally). · appears on 248 routes · implemented by `src/components/blog/CookieConsent.jsx (mounted in src/App.jsx)`

### HERO

_Page-opening block directly under the header._

**`hero.home-parallax`** — Homepage hero: 'Meet Riley' serif H1, sub-copy, primary CTA and hero illustration over four looping, scroll-parallaxed cloud layers.

· Homepage only (1 route). · appears on 1 routes · implemented by `src/components/Hero.jsx (+ upper/HeroParallaxClouds.jsx)`

**`hero.pricing-plans`** — Pricing hero: tangerine radial background with the reused cloud layers at 70% opacity, eyebrow, H1, two plan cards (Riley Plus+, Riley Basic) and a large CTA with arrow.

· Pricing only (1 route). · appears on 1 routes · implemented by `src/components/pricing/PricingHero.jsx (+ PlanCard.jsx, upper/HeroParallaxClouds.jsx)`

### PROOF

_Social proof: press logos, expert board, user testimonials._

**`proof.press-marquee`** — Lilac strip of press logos scrolling left in a 20s linear loop with edge fade mask; sits at the bottom of the homepage hero.

· Homepage only (1 route). · appears on 1 routes · implemented by `src/components/Hero.jsx > Marquee (upper/Marquee.jsx)`

**`proof.family-marquee`** — Personalisation heading over a row of parenting-style 'family' illustrations scrolling right in a 50s linear loop.

· Homepage only (1 route). · appears on 1 routes · implemented by `src/components/PersonalizationMarquee.jsx`

**`proof.clinical-board`** — Expert/clinical advisory board: doctor portraits with names and credentials.

· Homepage only (1 route). · appears on 1 routes · implemented by `src/components/ClinicalBoard.jsx`

**`proof.testimonial-carousel`** — Looping five-slide carousel of user quotes with avatar, stars and prev/next arrows.

· Homepage and pricing (2 routes). · appears on 2 routes · implemented by `src/components/Testimonials.jsx`

### PRODUCT

_Explains what Riley does and how it works._

**`product.superpowers-grid`** — Two-column grid of six parenting-challenge cards; each opens a full-screen modal with mascot, three feature cards and a CTA.

· Homepage only (1 route). · appears on 1 routes · implemented by `src/components/Superpowers.jsx (+ upper/SuperpowerModal.jsx)`

**`product.chat-featurette`** — Orange looping carousel of phone mockups playing Rive chat animations, with prev/next arrows and a 'Talk to Riley' CTA.

· Homepage only (1 route). · appears on 1 routes · implemented by `src/components/Featurette.jsx (+ upper/RiveChat.jsx, shared/useEmblaLoop.js)`

**`product.how-it-works`** — 'How Riley Works' explainer on the latte-100 background with large serif heading and step content.

· Homepage only (1 route). · appears on 1 routes · implemented by `src/components/HowRileyWorks.jsx`

**`product.feature-cards`** — Three coloured feature cards (apricot, lilac, marigold) at the top of the pink-orange gradient band.

· Homepage only (1 route); the pricing page renders the gradient band without it. · appears on 1 routes · implemented by `src/components/lower/FeatureCards.jsx (inside GradientBand.jsx)`

### CONVERSION

_Blocks whose job is to move the visitor to sign up or compare plans._

**`conversion.comparison-table`** — Riley-vs-alternatives feature matrix with filled/empty checks; header labels rotate at 960px and below.

· Homepage and pricing (2 routes), inside the gradient band. · appears on 2 routes · implemented by `src/components/lower/ComparisonTable.jsx (inside GradientBand.jsx)`

**`conversion.final-cta`** — Closing sign-up band with large serif heading, clouds, mascots and the primary CTA.

· 230 routes: homepage, pricing, the blog index, every category page and every article, directly above the footer. · appears on 230 routes · implemented by `src/components/FinalCta.jsx`

### SUPPORT

_Answers objections and questions._

**`support.faq-clouds`** — Large FAQ heading with question 'clouds'; opening one centres it and blurs the rest; background clouds slide aside 1s after the section enters view.

· Homepage and pricing (2 routes). · appears on 2 routes · implemented by `src/components/FaqClouds.jsx`

### CONTENT

_Entry points into editorial content._

**`content.blog-teaser`** — 'Explore the Riley Blog' block: category pills and three post cards; a horizontal snap scroller at 639px and below.

· Homepage only (1 route). · appears on 1 routes · implemented by `src/components/BlogTeaser.jsx`

### ERROR

_Error-state page bodies._

**`error.not-found`** — 'Playing peekaboo' 404 body: serif heading, one-line message, 'Go back' link and wide cloud illustration; sets robots noindex.

· 14 routes: the dead sitemap slugs and the linked-but-unbuilt paths (author/reviewer pages, /support), plus any unknown path via the router fallback. · appears on 14 routes · implemented by `src/pages/NotFound.jsx`

### BLOG

_Blog listing UI: discovery, filtering and paging of posts._

**`blog.index-hero`** — Mascot, 'Riley Articles' serif heading, subtitle and books illustration opening the blog listing.

· Blog index and every category page (7 routes). · appears on 7 routes · implemented by `src/components/blog/BlogIndexHero.jsx`

**`blog.search`** — Live type-ahead search box with a results dropdown; the clone filters blogPosts.json locally instead of calling the original's search API.

· Blog index and every category page (7 routes); articles embed the same component inside article.top-bar. · appears on 7 routes · implemented by `src/components/blog/BlogSearch.jsx`

**`blog.category-tabs`** — Row of category tabs (All plus six categories and Authors) with the active one highlighted; distinct from the homepage blog-teaser pills.

· Blog index and every category page (7 routes). · appears on 7 routes · implemented by `src/components/blog/BlogCategoryTabs.jsx`

**`blog.featured-banner`** — Large featured-post banner: horizontal at 992px and up, stacked below.

· Blog index and every category page (7 routes); empty on health and pregnancy, which have no featured posts. · appears on 7 routes · implemented by `src/components/blog/BlogFeaturedCard.jsx`

**`blog.post-grid`** — Grid of post cards (wide and normal variants) with category tag, title, excerpt, author and date; 6 posts per page on the index.

· Blog index and every category page (7 routes). · appears on 7 routes · implemented by `src/components/blog/BlogPostCard.jsx (+ CategoryTag.jsx)`

**`blog.pagination`** — 'Page N of M' control with prev/next links to /blog?page=N.

· Blog index and every category page (7 routes); category pages always show a single page. · appears on 7 routes · implemented by `src/components/blog/BlogPagination.jsx`

### ARTICLE

_Blocks of the single-article reading template._

**`article.top-bar`** — Back link plus search box at 992px and up; full-width search only below.

· All 221 articles. · appears on 221 routes · implemented by `src/components/article/ArticleTopBar.jsx`

**`article.breadcrumbs`** — Pill breadcrumb trail Home › Blog › Category › Title.

· All 221 articles. · appears on 221 routes · implemented by `src/components/article/ArticleBreadcrumbs.jsx`

**`article.header`** — Title, description, author and reviewer bylines, updated date and read time, top share buttons and the hero image.

· All 221 articles. · appears on 221 routes · implemented by `src/components/article/ArticleHeader.jsx (+ AuthorByline.jsx, ShareButtons.jsx)`

**`article.toc`** — 'In this article' table of contents: sticky side column at 992px and up, inline box below, with its own copy-link button.

· All 221 articles. · appears on 221 routes · implemented by `src/components/article/ArticleToc.jsx`

**`article.sources`** — 'N sources cited' collapsible list.

· All 221 articles. · appears on 221 routes · implemented by `src/components/article/SourcesAccordion.jsx`

**`article.share-row`** — Bottom row of share buttons and copy-link after the sources.

· All 221 articles. · appears on 221 routes · implemented by `src/components/article/ShareButtons.jsx (variant bottom)`

**`article.related-posts`** — 'You'll also love these posts:' heading with a carousel area and See All button; renders empty on the original, so empty in the clone too.

· All 221 articles. · appears on 221 routes · implemented by `src/components/article/RelatedPosts.jsx`

**`article.intro`** — Article lead-in: the blocks before the first H2 (opening paragraph with citation superscripts, optional promo unit). Body copy is placeholder in the clone.

· All 221 articles. · appears on 221 routes · implemented by `src/components/article/ArticleBody.jsx (+ PromoUnit.jsx)`

**`article.chapter`** — One H2-bounded chapter of the article body (H2, paragraphs, H3s, nested lists, images, editor's note, downloadable image); repeats once per H2.

· All 221 articles (repeatable). · appears on 221 routes · implemented by `src/components/article/ArticleBody.jsx (+ EditorNote, ArticleImage, DownloadableImage)`

### LEGAL

_Policy and editorial text-page bodies._

**`legal.policy-embed`** — Empty policy embed slot: the original's third-party policy embed is blocked by its own security policy, so the body renders 0px tall.

· The 3 legal routes (/tos, /privacy, /cookies). · appears on 3 routes · implemented by `src/pages/LegalPage.jsx`

### TEXT

_Text-page (editorial process) blocks, split at real heading boundaries._

**`text.header`** — Text-page title (bold H2) and intro paragraph; no horizontal padding (original quirk). Copy is placeholder in the clone.

· Editorial process only (1 route). · appears on 1 routes · implemented by `src/pages/TextPage.jsx`

**`text.chapter`** — One H3-bounded part of a text page: the H3 and its bullet list (optional bold lead labels); repeats once per H3.

· Editorial process only (1 route; one per level-three heading). · appears on 1 routes · implemented by `src/pages/TextPage.jsx`

**`text.closing`** — Closing paragraph with inline links (support form, full page on the original).

· Editorial process only (1 route). · appears on 1 routes · implemented by `src/pages/TextPage.jsx`
