# Riley clone — design-repo

An AI-ready, machine-validated design system for the Riley (rileyapp.com) clone. It lets a
generator compose new on-brand page specs (PageSpecs) without inventing colors, copy
budgets, sections, motion, or asset semantics. It is a **snapshot of the built clone**
(templates `home`, `pricing` and `not-found`), not a living mirror of the source project.

- **Status:** `design-review-pending`, `productionApproved: false` (see `registry.manifest.json`)
- **Theme:** `riley-light` only. No dark mode exists on the original or the clone.
- **Source project:** React 18.3 + Vite 5.4 + Tailwind 3.4 + `@rive-app/react-canvas` 4.36 clone of a
  Next.js + Tailwind v4 + framer-motion + embla + react-scroll-parallax + Rive original.
  The versions are machine-checked against `../package.json` by `extraction/verify_all.py`.

## Counts (recomputed from disk by `extraction/verify_all.py`)

| what | count |
|---|---|
| tokens: 00-foundation / 10-semantic / 20-component / 30-layout | 117 / 61 / 49 / 17 (total 244) |
| primitives (`primitives/*.json`, PascalCase) | 10 |
| components (`components/*.json`) | 16 |
| sections (`sections/*.json`) | 17 |
| templates (`templates/templates.json`) | 3 (home, pricing, not-found) |
| routes mapped | 11 (`/`, `/pricing`, 8 dead sitemap slugs, `*` catch-all) |
| excluded / pending route patterns | 9 |
| asset roles (closed enum) | 18 (14 pinned) |
| compatibility-graph rules | 19 |
| motion patterns (closed enum) | 10 |

<!-- counts:{"tokens":{"00-foundation":117,"10-semantic":61,"20-component":49,"30-layout":17,"total":244},"primitives":10,"components":16,"sections":17,"templates":3,"routesMapped":11,"deadSlugRoutes":8,"routesExcludedPatterns":9,"assetRoles":18,"graphRules":19,"motionPatterns":10} -->

## Layout

```
design-repo/
  README.md · CHANGELOG.md · registry.manifest.json
  tokens/00-foundation/   color, gradient, typography, breakpoint, radius, elevation, motion
  tokens/10-semantic/     color-roles, typography-roles, motion-roles
  tokens/20-component/    button, card, pill, table, nav
  tokens/30-layout/       container, section-spacing
  tokens/themes/          riley-light (semantic -> foundation, resolved)
  tokens/llm/             component-allowlist, token-catalog, token-policy
  primitives/             Button, TextLink, CategoryPill, Avatar, Icon, Image, Text, RoundArrowButton, CheckMark, Divider
  components/             marquee, parallax-cloud-stack, embla-loop-carousel, superpower-card, ... (16)
  sections/               17 section contracts (content budget, constraints, motion, structured responsive, evidence)
  templates/templates.json  3 templates as {section, required, repeatable, variant} nodes + routes + exclusions + content policy
  compatibility/graph.json  19 rules, each with severity error|warn and named exceptions
  animation/motion-spec.json  closed motion patterns, M1-M15 inventory, QA corrections
  assets/asset-roles.json + assets/README.md  closed asset-role enum with generation/licensing policy
  schema/pagespec.schema.json  draft-07, closed enums, additionalProperties:false everywhere
  schema/example.pagespec.json the full home page with real short UI copy
  schema/validate_schema.py    Draft7Validator run
  schema/semantic_validate.py  everything JSON Schema cannot express (one function per graph rule)
  schema/tests/adversarial_test.py  controls + mutations
  extraction/measured-values.json   citation ledger (build-time evidence outside this folder)
  extraction/verify_all.py          drift-proof repo checks
```

## Commands (run from this folder; requires Python 3.9+ and `jsonschema`)

```bash
python3 schema/validate_schema.py          # Draft7Validator on the example -> 0 errors
python3 schema/semantic_validate.py        # schema + 19 graph rules on the example (or pass PageSpec paths)
python3 schema/tests/adversarial_test.py   # 6 controls pass, 30 mutations rejected
python3 extraction/verify_all.py           # repo-level drift checks (see its docstring)
```

Every script derives the repo root from `__file__`, so they run unchanged from any copy.
When the folder is shipped alone, with no sibling source project, `verify_all.py` turns the
citation, route-source, asset-file, IA and version cross-checks into **WARN** lines. It still
runs every internal check.

## How a generator uses it

1. Pick a `template` (`home` | `pricing` | `not-found`). The PageSpec's `nodes` must reproduce
   that template's node list in order, keyed on `(section, variant)`. Every node in every
   template is required and non-repeatable, because the clone has exactly one composition per
   page shape.
2. Fill each node's `content` within the `x-maxWords` budgets (`sections/<id>.json`
   `contentContract.copyBudget`). Each budget is the real copy length plus about 20–30%.
3. Set `motion` to the section's single allowed `pattern`, plus its const-locked
   `reducedMotionFallback`.
4. Reference media and links only through `assetRole`. A PageSpec has **no href/URL field
   anywhere**, so live endpoints cannot be smuggled in.
5. Set `page.brandContext`. `other-brand` forbids every `must-reuse-exact`,
   `must-not-fabricate` and `must-not-reuse-live-endpoint` role. In practice, none of the three
   Riley templates can be emitted verbatim for another brand.

## Scope, routes and things deliberately NOT normalised away

- **Dead sitemap slugs.** `/baby-tracker`, `/sleep-tracker`, `/sleep-training`,
  `/sleep-regression`, `/all-in-one`, `/your-babys-sleep-simplified`, `/product-hunt` and
  `/give-the-gift` are soft-404s on the live original and in Wayback 2025. They map to the
  `not-found` template and **must not be recreated as landing pages**. This is enforced by
  `ROUTE_TEMPLATE_BINDING` and the adversarial case "dead sitemap slug bound to landing
  template". `verify_all.py` pins the exact set of 8.
- **Excluded / pending routes.** These are listed in `templates.json` `excludedRoutes`, each
  with a reason: `/blog`, `/blog/{category}`, `/blog/author/{slug}`,
  `/blog/{category}/{slug}`, `/editorial-process`, `/tos`, `/privacy`, `/cookies`, and
  `/support` (UNVERIFIED). A PageSpec targeting one is rejected.
  **While this snapshot was being built, a concurrent agent landed the blog, text and legal
  pages in the source** (`src/pages/routes.jsx`, `BlogIndexPage.jsx`, `BlogArticlePage.jsx`,
  `TextPage.jsx`, `LegalPage.jsx`). They remain excluded here. `verify_all.py` prints a WARN
  for each source route that is built but not modelled, so the gap stays visible. Rebuild this
  design-repo to model them.
- **Content policy.** Blog article bodies and legal/text-page copy are intentionally
  placeholder in the clone (long-form text was not copied). Testimonials, clinician
  names/credentials, plan prices and competitor comparison marks are real-world claims. Reuse
  them only in `riley-clone`, and never fabricate them.
- **Global overlay not modelled.** `App.jsx` now renders a fixed `CookieConsent` bar on every
  route. It landed with the blog work and is recorded in
  `templates.json` `unmodelledGlobalOverlays`.
- **GradientBand.** The IA (`../ia.json`) splits it into `product.feature-cards` and
  `conversion.comparison-table`. Here it is one real wrapper node with variants
  `feature-cards-and-table` (home) and `table-only` (pricing). Each section's `iaSectionIds`
  holds the crosswalk, which `verify_all.py` checks.
- **Type quirks kept on purpose.** Bold Cadiz faces compute `font-weight: 400` (the family is
  swapped, not the weight). The `h1` / `desktop-*` / `mobile-*` rules are unlayered so they
  beat utilities.

## Motion

- There is no scroll-reveal anywhere (measured). The closed motion enums make it
  impossible to add one.
- Live animation-pass values outrank CLONE_SPEC §14. Independent animation-QA corrections are
  applied:
  - no superpower-card hover (cursor `auto`)
  - the mobile-menu slide is approximate (original ~264ms JS-driven)
  - header fixes at ~54–55px
  - blog hover animates the `scale` property
  - featurette drag follows the pointer from anywhere, incl. the Rive canvas (earlier "no follow" reading was a timing artifact); touch fixed
- The clone has **no** `prefers-reduced-motion` handling, so every `reducedMotionFallback` is
  prescriptive guidance, not measured behaviour.

## Versioning

`allowlistVersion` and `pageSpecVersion` are machine-checked by `verify_all.py`.
`repositoryVersion` is documentation-only. See `registry.manifest.json` `versionFieldNote`.

## Packaging

Build `design-repo.zip` last, from the parent folder, with the CLI:
`zip -r -X design-repo.zip design-repo -x '*.DS_Store' -x '__MACOSX/*' -x '*/__pycache__/*'`.
The source project is **not a git repository**, so the "zip committed to git" check is N/A. If
it becomes one, add `design-repo.zip` to `.gitignore` and confirm with `git ls-files`.

## Known gaps

- The Rive chat content and timing live inside the `.riv` files and can't be measured.
- Several CTA destinations are UNVERIFIED (role `unspecified-destination`).
- The mobile-menu blog sub-links (M15) are UNVERIFIED and not rendered.
- `/support` is linked from the footer, but its live status is unknown.
