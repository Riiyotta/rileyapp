Source: https://rileyapp.com/

# Asset manifest: rileyapp.com homepage

All paths are relative to `/Users/riyaghosh/V3/rileyapp/public` (serve as `/assets/...`, `/fonts/...`).
"Live URL" is the original path on rileyapp.com. Every file in `public/assets/` that came from the saved `_files` folder was checked by MD5 against the live original and matches byte-for-byte.

## Fonts (`/fonts/`), downloaded from `/_next/static/media/*.woff2`

| File | Live file | CSS family alias on site | Declared weight | Real typeface (from the WOFF2 name table) |
|---|---|---|---|---|
| Cadiz-Regular.woff2 | 21e981d7c49f3a54-s.p.woff2 | sansRegular | 400 | Cadiz Regular |
| Cadiz-RegularItalic.woff2 | 70b85aac0364cf97-s.p.woff2 | sansRegularItalic | 400 | Cadiz Regular Italic |
| Cadiz-Book.woff2 | e50b6ebb6bce841c-s.p.woff2 | sansBook | 350 | Cadiz Book |
| Cadiz-BookItalic.woff2 | d84e7a84fb22f8cf-s.p.woff2 | sansBookItalic | 350 | Cadiz Book Italic |
| Cadiz-SemiBold.woff2 | a038179073b22d98-s.p.woff2 | sansSemibold | 600 | Cadiz SemiBold |
| Cadiz-SemiBoldItalic.woff2 | 445937849f5b9b72-s.p.woff2 | sansSemiboldItalic | 600 | Cadiz SemiBold Italic |
| Cadiz-Bold.woff2 | 3665f82e521e4c2c-s.p.woff2 | sansBold | 700 | Cadiz Bold |
| Cadiz-BoldItalic.woff2 | 4a3aef181986093c-s.p.woff2 | sansBoldItalic | 700 | Cadiz Bold Italic |
| Cadiz-Black.woff2 | 9991ff847b152bd7-s.p.woff2 | sansBlack | 800 | Cadiz Black |
| Cadiz-BlackItalic.woff2 | 099e556d489a07c0-s.p.woff2 | sansBlackItalic | 800 | Cadiz Black Italic |
| Recoleta-Regular.woff2 | cd6e05420753477e-s.p.woff2 | "serif" | 400 | Recoleta Regular |

The homepage uses these families: sansRegular, sansBold, sansSemibold, and "serif" (Recoleta). The others are declared but not used here.

## Raster/SVG images (`/assets/`)

| Local file | Live URL | Used in | Intrinsic | Rendered @1440 |
|---|---|---|---|---|
| wordmark.svg | /_next/static/media/wordmark.9c6f1ca2.svg | Header logo | 79x52 aspect | 79x52 |
| HeroRiley.svg (= HeroRiley(1).svg) | /_next/static/media/HeroRiley.7fe0f1f7.svg | Inline mascot in H1 (lg+), mobile mascot above H1 (<lg) | 77x84 | 72x78.5 (lg), 92.8x101.2 (<lg) |
| HeroIllo.84fc0736.svg | /_next/static/media/HeroIllo.84fc0736.svg | Hero illustration | 1092x952 | 640x558 box, scale(2) → 1280x1116 visual |
| nbc.png, axios.png, bump-logo.png, finsmes.png, tc.png, glamour.png | /_next/static/media/{nbc.d05d499b,axios.3f8939b8,bump-logo.f34c9e6e,finsmes.98719778,tc.510556fc,glamour.185eac21}.png | Press marquee | 392x96, 380x96, 800x154, 239x24, 714x120, 425x96 | 128 wide, max-h 24 (object-contain) |
| softie-family.svg, spark-family.svg, uplifter-family.svg, riley-family.svg, worrier-family.svg, guide-family.svg | /_next/static/media/*-family.*.svg | Family marquee (section 2) | aspect 168/194, 168/132, 168/110, 168/132, 168/153, 168/123 | h 164; w 142 / 208.7 / 250.5 / 208.7 / 180.1 / 224 |
| bottle.svg, moon.svg, blocks.svg, stubborn.svg, bowl.svg, sailboat.svg | /icons/*.svg | Superpower cards | 143,143,84,65,56x49,55x41 | 40x40 object-contain |
| mascot.svg | /_next/static/media/mascot.f7858b88.svg | Superpower section (bottom-left) | 177x179 | 177x179 |
| background-clouds.svg | /_next/static/media/background-clouds.29b46e22.svg | Featurette orange card bg | 1440x740 | fills card, scale 1.25 |
| background-clouds(1).svg | /_next/static/media/background-clouds.0c94200b.svg | Final CTA background | 1774x826 | 1440x670.5 |
| phonebg.svg | /_next/static/media/phonebg.f9a0e650.svg | Featurette phone shell | 464x593 (370x473 natural) | 511x601 (top inset 8px), object-contain |
| meg.png, seb-and-daughter.png, naina.png | /images/homepage/featurette/*.png | Featurette right image | 1470x1653 | 491x551.7 |
| lilly.png, kate.png | /_next/static/media/{lilly.e941c573,kate.a02b9b6f}.png | Clinical board portraits | (large PNG) | 362x365.7 |
| worrier-family.svg, guide-family.svg, spark-family.svg | /mascots/*-family.svg (identical bytes to the /_next/static/media versions) | How Riley Works | 112x102, 140x102, 140x110 | 214 wide (195.3 / 156.3 / 168 tall) |
| purple1.svg … purple5.svg | https://a.storyblok.com/f/337915/…/purpleN.svg | Testimonial avatars | 62x61 / 60x61 | 64x64 rounded-full object-cover |
| chat.svg, tracking.svg, sparks.svg | /_next/static/media/{chat.8b820a89,tracking.f65b62b2,sparks.372f2bdd}.svg | Feature cards | aspect 333/167 | 327x164 (chat), 291.5x146.2 (others) |
| 4.png, 5.png, 3.png, 2.png, 6.png | https://a.storyblok.com/f/337915/500x500/…/N.png | FAQ portraits (order 4,5,3,2,6) | 500x500 | 40x40 rounded-full object-cover |
| riley-up.svg | /_next/static/media/riley-up.80680fc4.svg | FAQ answer mascot | 102x83 | 98.3x80 |
| 3dd009c0…-5760x3840.jpeg, 6ec23763…-5744x3829.jpeg, 8fe3a7b3…-1600x1066.jpeg | https://cdn.sanity.io/images/antwkw01/development/*.jpg | Blog cards | 5760x3840, 5744x3829, 1600x1066 | 288x352 object-cover |
| mascots.svg | /_next/static/media/mascots.ad5f2082.svg | Final CTA bottom mascots | aspect 778/97 | 680x192 |

Duplicates: `HeroRiley(1).svg`, `guide-family(1).svg`, `spark-family(1).svg`, `worrier-family(1).svg` are byte-identical duplicates.

## Downloaded in this run

| Local file | Live URL | Notes |
|---|---|---|
| assets/animations/chat_module_meg.riv | /animations/featurette/chat_module_meg.riv | Rive file, 443,466 bytes. All 3 .riv files are byte-identical; each slide picks a different artboard/state machine (see spec). |
| assets/animations/chat_module_seb.riv | /animations/featurette/chat_module_seb.riv | same bytes |
| assets/animations/chat_module_naina.riv | /animations/featurette/chat_module_naina.riv | same bytes |
| assets/modal/mascots/{worrier,guide,softie,spark,uplifter,explorer}.svg | /mascots/*.svg | Superpower modal header mascots |
| assets/modal/icons/{puzzle,ruler,handsTogether,lightbulb,knight,ladder,affectionate,music,independent,books,heartParachute,octopus,everything,calendar,magicWand,rocket,elephant}.svg | /icons/*.svg | Superpower modal item icons |

Missing on the live site: `/icons/curious.svg` and `/icons/friendly.svg` return an HTML soft-404 (HTTP 200, text/html), so those images are broken on the original. Nothing was saved for them.

## Inline SVGs extracted (`/assets/icons/`)

| File | Where | Size | Notes |
|---|---|---|---|
| hero-cloud-1.svg | Hero parallax layers 1 & 3 | 411x251 | white→#FCFBF7 linear-gradient cloud |
| hero-cloud-2.svg | Hero parallax layer 2 | 592x362 | |
| hero-cloud-3.svg | Hero parallax layers 2 & 3 | 411x251 | variant |
| hero-cloud-4.svg | Hero parallax layer 4 (foreground) | viewBox 592x362, rendered 473.6x289.6 | |
| menu-hamburger.svg / menu-close.svg | Mobile header toggle | 28x23 / 23x24 | stroke/fill #2E2A42 |
| apple-logo.svg | Hero "Available on:" | 14x16 | fill black |
| card-arrow.svg | Superpower card right arrow | 13x12 | fill #5934C5, stroke #7A55FD 0.125 |
| featurette-prev.svg / featurette-next.svg | Featurette carousel buttons | 13x13 | next = same path + `rotate-180` |
| review-prev.svg / review-next.svg | Testimonial carousel buttons | 13x13 | fill #5934C5 stroke #7A55FD |
| stars-5.svg | Testimonial rating | 198x38 | 5 stars fill #FFDD7D |
| table-check-filled.svg | Comparison table "yes" | 29x29 (vb 30x30) | circle fill #5934C5 stroke #2E2A42 1.206, white check |
| table-check-empty.svg | Comparison table "no" | 31x30 | circle fill transparent stroke #2E2A42, white check (invisible on white) |
| faq-plus.svg | FAQ summary toggle | 19x19 | fill #5934C5; rotates 135deg when open |
| faq-cloud-1..5.svg | FAQ background clouds | 452x276, 326x199, 244x149, 383x167, 401x246 | gradient ids clash if inlined together; use as <img> or rename ids |
| footer-divider.svg | Footer column separators (lg+) | 1x142 | black 0.5 opacity stroke 0.5 |
| app-store-badge.svg | Footer "Get the App" | 153x52 | link https://rileyapp.onelink.me/JNxh/ln83navr |
| footer-logo.svg | Footer bottom logo | 118x76 | fill #2E2A42 |
