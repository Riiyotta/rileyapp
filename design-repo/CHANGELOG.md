# Changelog

## 2.0.0 — reconcile with the latest clone; clone/generation modes; non-SaaS policy binding

Review items (Situation B; each verified against the real repo first):
- Re-extraction from the latest runnable clone (`npm ci` + `vite build` OK): routes enumerated from
  `src/pages/routes.jsx` + `src/data/blogPosts.json`; 249 routes mapped exactly once, `excludedRoutes` now empty.
- New families: blog listing (`blog-index`, `blog-category`), article (`blog-article`), text page (`text-page`),
  legal (`legal`). Author pages did NOT reproduce as a page family: the clone links to them but never built them,
  so `/blog/authors`, `/blog/author/*`, `/blog/reviewer/kate-roche` and `/support` map to `not-found` (`unbuiltLink`).
- 19 new section contracts (36 total), 10 new components; article split at H2 (intro + chapters + meta + related),
  editorial page split at H3; legal stays an empty embed slot because the clone renders no legal text.
- Measured section heights at 1440 (+768/390) from the built clone (`extraction/measure_sections.mjs`); typography
  recheck at 3 viewports; new tokens for blog/article colours, type steps, radii and spacing (all cited).
- Compatibility graph: 41 rules (was 19) incl. generation-mode, token, retrieval and article rules.
- PageSpec 2.0.0: required closed `page.mode` (`clone` | `generation`) replaces `brandContext`; optional `page.brand`,
  `node.style` (token refs) and `overlays`; examples moved to `schema/examples/` (8 clone, 7 generated).
- Leakage registry `schema/leakage-patterns.json` built by `extraction/build_leakage_patterns.py` (brand, persons,
  press/competitors, claims, domains, embed ids, store marks, ratings, 5-word shingle hashes).
- Asset roles: three-way availability + substitutes + guidance; 8 generation-safe roles + 5 new source roles
  (article covers, author avatars, social marks, policy embed, source citations); `PINNED_AVAILABILITY` in both validators.
- Baseline R7/R8/R9/R10: `source`/`semantic` split (`build_provenance.py`), closed `schema/section-contract.schema.json`,
  `retrievalEligible` pins, `wrapper_gate.py` + whitelist, generated token catalog + token policy rules.
- Non-SaaS policy: `policy/design-policy.json` (`consumer-parenting-app-web`, isSaaS false, notBoundTo the SaaS
  common policy, consumer-app generation rules); manifest `category: consumer-app` + `designPolicy` with a
  recomputed `contentHash`.
- `extraction/prove_drift.py` (new): every pin, gate and parity check proven against a scratch copy.
- Root IA (`ia.json`, `IA.md`, `matrix.csv`) reconciled: article body / editorial prose sections replaced by the
  decomposed ones; unbuilt links mapped to the 404 template; `node validate.mjs` reconciles.

Honesty: no human reviewed the pinned patterns, roles or policy (agent attestation, not a human sign-off);
leakage detection is string-based; live-vs-clone visual parity was not measured.

## 1.0.1 — re-sync after the animation-fix pass

- Source project is now a git repo: README and manifest packaging notes updated; `design-repo.zip`
  is gitignored and confirmed untracked via `git ls-files`.

- Featurette: drag/touch claims corrected in sections/featurette-carousel.json, animation/motion-spec.json
  (M6), extraction/measured-values.json and README. The original drags 1:1 from anywhere; the earlier
  "slow drag does not follow" reading was a headless frame-starvation artifact. Clone touch swipe fixed.
- Blog image hover: clone now animates the CSS `scale` property like the original (M13 value + 2 anchors).
- Hero illustration: now CSS `scale`/`translate` properties (hero-home anchor + prose).
- Parallax: progress formula re-cited (HeroParallaxClouds.jsx:91, :91-103); added the original's
  frozen-banner-height rule used for homepage layer heights.

## 1.0.0 — initial build (snapshot of the built clone: home, pricing, not-found)

- Tokens: 244 evidence-cited tokens across 00-foundation / 10-semantic / 20-component / 30-layout,
  all from `tailwind.config.js`, `src/index.css`, `src/styles/*.css` and CLONE_SPEC.md (no
  invented colors). Theme `riley-light` resolves every semantic color role.
- 10 primitives, 16 components, 17 sections, 3 templates, 19 graph rules, 18 asset roles,
  10 motion patterns.
- PageSpec schema (draft-07): closed template, type, motion-pattern and assetRole enums;
  `additionalProperties:false` everywhere; gradient-band variants as a `oneOf` of independent
  node schemas; `motion` is required with a const `reducedMotionFallback`; no href/URL field.
- `schema/semantic_validate.py`: one function per graph rule. Severity and exceptions are read
  from `compatibility/graph.json`, and the validator refuses to run if the rule-id sets differ.
- `schema/tests/adversarial_test.py`: controls auto-synthesized per template, plus 30 mutations.
- `extraction/verify_all.py`: allowlist parity, version parity, recomputed counts (manifest and
  README), citation range plus content-anchor check, pinned asset roles, route coverage
  (including source router and href scan), absolute-path scan, entry points, graph/validator
  agreement, referenced scripts, responsive structure, copy-budget parity, token policy,
  theme, framework versions, and the IA crosswalk.
- Applied the independent animation-QA corrections (superpower hover removed, mobile-menu
  timing approximate, sticky threshold ~54–55, blog `scale` property, featurette drag/touch).
- Concurrent source changes during the build: the blog/text/legal pages and `routes.jsx`
  landed (kept excluded/pending here, WARN in verify_all), `Button.jsx` gained a `colors`
  prop, `App.jsx` gained `CookieConsent`, and `ia.json` was restructured. Citations into the
  moved files were re-resolved by content anchor, and every shift was reviewed.
- Authoring note: the JSON files were produced by one-off scratch builder scripts kept outside
  this folder. The JSON on disk is the source of truth.
