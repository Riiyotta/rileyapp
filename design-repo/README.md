# Riley clone — design-repo (2.0.0)

An AI-ready, machine-validated design system for the Riley (rileyapp.com) clone: tokens, primitives, components,
36 section contracts, 8 templates in 7 families, a closed PageSpec schema with a semantic validator, adversarial and
drift proofs. It is a **snapshot of the latest runnable clone** (git `2495803`), not a living mirror.

- **Status:** `design-review-pending`, `productionApproved: false`. Nothing here has been reviewed by a human.
- **Category / policy:** `consumer-app`, bound to the non-SaaS policy `policy/design-policy.json`
  (`consumer-parenting-app-web` 1.0.0, Common IR 0.5, `isSaaS: false`, explicitly **not** bound to
  `n0-saas-design-constraints-common`). Decision state: `defined-pending-architecture-review` — an agent wrote the
  classification (agent attestation, not a human sign-off).
- **Theme:** `riley-light` only (no dark mode exists on the original or the clone).
- **Source stack (documentation only):** React 18 + Vite 5 + Tailwind 3 clone of a Next.js original; versions are
  machine-checked against `../package.json`.

## Counts (recomputed from disk by `extraction/verify_all.py`)

| what | count |
|---|---|
| tokens 00-foundation / 10-semantic / 20-component / 30-layout | 147 / 77 / 49 / 21 (total 294; catalog 294) |
| primitives / components / sections | 10 / 26 / 36 |
| templates (families) | 8 (7) |
| routes mapped (incl. `*`) | 249 (221 articles, 8 dead slugs, 6 unbuilt links) |
| excluded routes | 0 |
| asset roles | 31 |
| compatibility-graph rules | 41 |
| motion patterns | 12 |
| example PageSpecs (clone / generated) | 8 / 7 |

<!-- counts:{"tokens":{"00-foundation":147,"10-semantic":77,"20-component":49,"30-layout":21,"total":294},"catalogTokens":294,"primitives":10,"components":26,"sections":36,"templates":8,"templateFamilies":7,"routesMapped":249,"articleRoutes":221,"deadSlugRoutes":8,"unbuiltLinkRoutes":6,"routesExcludedPatterns":0,"assetRoles":31,"graphRules":41,"motionPatterns":12,"examples":{"clone":8,"generated":7}} -->

## Commands (run from this folder; Python 3.9+ with `jsonschema`)

```bash
python3 schema/validate_schema.py              # Draft-07 on every schema/examples/*.pagespec.json
python3 schema/semantic_validate.py            # schema + all graph rules on every example (or pass paths)
python3 schema/tests/adversarial_test.py       # controls pass; every PageSpec / registry / gate mutation rejected
python3 extraction/verify_all.py               # repo-level checks (see its docstring)
python3 extraction/prove_drift.py --scratch DIR   # each pin/gate/parity check proven to catch drift in a scratch copy
python3 extraction/wrapper_gate.py             # R9 gate alone
python3 extraction/build_provenance.py --check        # R7 source{} re-derived from implementedBy
python3 extraction/build_leakage_patterns.py --check  # generation-mode patterns re-derived from the real source
python3 extraction/build_token_catalog.py --check     # catalog re-derived from the token files
python3 extraction/policy_hash.py              # contentHash of the files the policy is enforced by
```

Re-measuring section heights (optional; needs the source project, Node and a global Playwright):
`npm ci && npx vite build --outDir <scratch> && npx vite preview --outDir <scratch> --port <port>`, then
`NODE_PATH="$(npm root -g)" RILEY_BASE_URL=http://localhost:<port> node design-repo/extraction/measure_sections.mjs`.

Every script derives the repo root from `__file__`. Shipped alone (no sibling source project), `verify_all.py`
turns citation, provenance, route-source, leakage-rebuild, asset-file, IA and version cross-checks into WARN lines
and still runs every internal check.

## Modes (`page.mode`, required, closed)

- **`clone`** — faithful reconstruction of this clone. Real Riley assets and copy are allowed as evidence, but
  restricted roles must use their registered files (`REGISTERED_ASSET_REF`).
- **`generation`** — a new page for another brand (`page.brand` required). Twelve named rules reject source
  identity and content: `GENERATION_MODE_BRAND`, `_ASSET`, `_PERSON`, `_CUSTOMER`, `_SCREENSHOT`, `_COPY`, `_CLAIM`,
  `_RATING`, `_STORE`, `_URL`, `_EMBED` (plus asset availability). Patterns live in `schema/leakage-patterns.json`,
  built by `extraction/build_leakage_patterns.py` from `src/`, `src/data/blogPosts.json` and the CLONE_SPEC files with
  file:line evidence; source copy is stored only as hashed 5-word shingles. Strings are normalised first (NFKC,
  zero-width removal, Cyrillic/Greek homoglyphs, curly quotes, dash variants).
  **Caveats:** no human reviewed these patterns; detection is string-based (paraphrase, translation or text in images
  evades it); the generic health-claim / rating phrasings in `policy` are policy-derived, not source-derived.
- Asset roles carry a closed `availability` (`clone-only` | `generation-safe` | `blocked-for-generation`), pinned in
  code in **both** validators (`PINNED_AVAILABILITY`), with `generationSafeSubstitutes` and `generatedModeGuidance`.
  Generation-safe roles: placeholder brand mark, user-supplied asset, generated illustration, placeholder
  screenshot, fictional person avatar, placeholder logo, placeholder URL (`.example` / `.invalid` only), original copy.

## Templates, routes and measured heights (built clone, 1440x900)

Every route the clone serves is mapped exactly once (`templates/templates.json`): the 7 exact routes, the 6
category pages, one route per post in `src/data/blogPosts.json` (221), the 8 dead sitemap slugs, 6 linked-but-unbuilt
paths (`/blog/authors`, three `/blog/author/<slug>`, `/blog/reviewer/kate-roche`, `/support` — the clone serves the 404
template for them) and the `*` fallback. `/blog?page=N` are views of `/blog`.

| template | family | routes | measured route | page px | tallest non-shell section |
|---|---|---:|---|---:|---|
| `home` | marketing-home | 1 | `/` | 11465 | gradient-band 2078px (18%) |
| `pricing` | pricing | 1 | `/pricing` | 5644 | gradient-band 1250px (22%) |
| `not-found` | error | 15 | `/baby-tracker` | 1478 | not-found-block 850px (58%) |
| `blog-index` | blog-listing | 1 | `/blog` | 4794 | blog-post-grid 2188px (46%) |
| `blog-category` | blog-listing | 6 | `/blog/sleep` | 3119 | final-cta 708px (23%) |
| `blog-article` | article | 221 | `/blog/sleep/baby-witching-hour` | 6607 | article-chapter 1081px (16%) |
| `text-page` | text-page | 1 | `/editorial-process` | 2136 | text-page-chapter 388px (18%) |
| `legal` | legal | 3 | `/tos` | 900 | legal-policy-embed 0px (0%) |

## Decomposition (R6) and retrieval (R8)

- Article bodies are split at real H2 boundaries: `article-intro` + repeatable `article-chapter`, with
  `article-header` (incl. breadcrumbs), `article-toc`, `article-sources`, `article-share-row`, `article-related-posts`.
- The editorial text page is split at real H3 boundaries: `text-page-header` + repeatable `text-page-chapter` +
  `text-page-closing`.
- Legal pages: the clone (like the original, whose third-party embed is blocked by its own CSP) renders an **empty**
  policy-embed slot — there is no legal text or heading to split, so legal is `legal-policy-embed` only. Generation
  mode never generates legal text; the slot points at an operator URL.
- `cookie-consent` is a global overlay: `retrievalEligible: false`, carried in `PageSpec.overlays`, rejected in
  `nodes[]` (`RETRIEVAL_INELIGIBLE_NODE`), pinned in both validators; `superpower-modal` and `mobile-menu` components
  are pinned ineligible too.
- `extraction/wrapper_gate.py` (HERO > 1800 warn / > 3000 error; one section > 50% warn / > 60% error; missing
  measurement or wrong viewport = error) passes with no hits and an empty whitelist.

## Tokens (R10)

`tokens/llm/token-catalog.json` lists every token by canonical path (built from the token files);
`token-policy.json` maps PageSpec `node.style` properties to catalog categories. `TOKEN_UNKNOWN`, `TOKEN_RAW_COLOR`,
`TOKEN_ARBITRARY_SPACING`, `TOKEN_UNSUPPORTED_FONT` and `TOKEN_THEME_COMBINATION` enforce it. 2.0.0 adds the
blog/article colours (category tints, promo gradient, borders), type steps (article body/h2/h3, blog titles, tabs)
and radii, each cited to the clone source; the typography recheck at 1440/768/390 is in
`extraction/measured-values.json` `typographyRecheck`.

## Things deliberately NOT normalised away

- **Dead sitemap slugs** map to `not-found` and must never become landing pages (`ROUTE_TEMPLATE_BINDING`).
- **Author / reviewer pages are not a page family here.** The clone links to them but never built them (the blog
  recon marked them out of scope); they render the 404 template, so they map to `not-found` (`unbuiltLink`).
- **Placeholder long-form copy.** Article bodies and the editorial page are placeholder text in the clone; their
  copy budgets are generation guidance, not measured against Riley's real article text.
- **GradientBand** stays one wrapper node with variants (`feature-cards-and-table` on home, `table-only` on pricing).
- **Type quirks**: bold Cadiz faces compute `font-weight: 400`; the `h1`/`desktop-*`/`mobile-*` rules stay unlayered.
- **Motion**: no scroll-reveal exists; the clone has no `prefers-reduced-motion` handling, so every
  `reducedMotionFallback` is prescriptive.

## Known gaps / honesty notes

- No human has reviewed the leakage patterns, the asset-role pins, the policy classification or the wrapper
  whitelist. Agent attestation is not a human sign-off.
- Live-vs-clone visual parity was **not** measured in this pass (no live capture was taken); the heights above are
  of the built clone only.
- Rive chat content lives inside `.riv` files and cannot be measured. Several CTA destinations are UNVERIFIED.
- Generation-mode leakage detection is string-based and can be evaded by paraphrase.

## Packaging

`design-repo.zip` is gitignored and never committed. If needed, build it last from the parent folder:
`zip -r -X design-repo.zip design-repo -x '*.DS_Store' -x '__MACOSX/*' -x '*/__pycache__/*'`.
