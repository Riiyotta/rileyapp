# Riley clone — information architecture

Local React + Vite + Tailwind v3 clone of https://rileyapp.com/. The site map lives in data:

- **`ia.json`** — the only file to hand-edit. Templates, routes and sections; each section is defined once and referenced by id.
- **`IA.md`** and **`matrix.csv`** — **generated** by `build.mjs`. Don't edit them; they get overwritten.

```bash
node validate.mjs   # checks route/template totals, section references, categories
node build.mjs      # regenerates IA.md and matrix.csv
```

Re-run both after any change to `ia.json`.

## Scope

242 of the site's 245 routes are mapped across 8 templates, all specced and built:

| Template | Routes | Evidence |
|---|---:|---|
| Blog article | 221 | `CLONE_SPEC_PAGES_BLOG.md` |
| 404 (dead landing slugs) | 8 | `CLONE_SPEC_PAGES_MARKETING.md` |
| Blog category | 6 | `CLONE_SPEC_PAGES_BLOG.md` |
| Legal policy | 3 | `CLONE_SPEC_PAGES_BLOG.md` |
| Homepage | 1 | `CLONE_SPEC.md` |
| Pricing | 1 | `CLONE_SPEC_PAGES_MARKETING.md` |
| Blog index | 1 | `CLONE_SPEC_PAGES_BLOG.md` |
| Editorial process | 1 | `CLONE_SPEC_PAGES_BLOG.md` |

The 3 author pages (`/blog/author/{slug}`) are in `meta.pendingRoutes`: they're out of scope and fall through to the 404 in the clone. The 37 `/blog?page=N` views are query strings on the blog index, not separate routes.

## What the data shows

- **One template is 91% of the site.** The article template covers 221 of 242 routes, so its 8 single-use sections (top bar, breadcrumbs, header, TOC, body, sources, share row, related posts) are where layout bugs would repeat most often. They're still page-local because no other template uses them.
- **Chrome splits two ways.** 15 routes carry the full frame including the announcement bar; the 227 category and article routes drop it. The header, footer and cookie banner are on every mapped route.
- **The final CTA is the most reused content block**, on 230 routes across 5 templates. The blog listing sections are shared by exactly two templates, the index and category pages, which are the same component with a category prop.
- **The homepage is still the most varied page.** 9 of its 17 sections appear nowhere else, so keep them page-local until a second page needs one.
- **Some pages copy gaps in the original.** All 8 landing slugs in the sitemap are 404s on the live site, the legal pages render an empty body because the original blocks its own policy embed, and the related-posts carousel is empty on every article. The clone matches each of these on purpose; don't "fix" them into new designs.

Article bodies and editorial copy are placeholder text in the clone; titles, metadata and thumbnails are real.

Every section names the component that renders it in `implementedBy`, so `IA.md` doubles as a map of `src/`.
