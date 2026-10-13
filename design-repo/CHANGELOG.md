# Changelog

## 1.0.1 — re-sync after the animation-fix pass

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
