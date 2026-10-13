# Asset roles

`assets/asset-roles.json` is a closed enum of 18 roles. They are derived from the real JSX
usage sites (`usageSites` cites), and the same set is wired through the schema (each media or
link field allows only its own roles), the allowlist (`assetRoles`), and the example PageSpec.
PageSpec media is `{assetRole, assetRef, alt?}`. Links are `{label, assetRole}` and never carry
an href.

| role | policy | weight | what |
|---|---|---|---|
| brand-wordmark | must-reuse-exact | proprietary brand mark | wordmark.svg, footer-logo.svg |
| mascot-illustration | must-reuse-exact | character IP | HeroRiley, mascot, riley-up, mascots, modal/mascots/* |
| mascot-family-mark | must-reuse-exact | character IP | *-family.svg |
| mascot-avatar | must-reuse-exact | character IP | purple1–5.svg (mascot cloud faces, not photos) |
| brand-illustration | must-reuse-exact | artwork | HeroIllo, 404 background, chat/tracking/sparks, phonebg |
| rive-animation | must-reuse-exact | artwork | animations/*.riv |
| press-logo | must-not-fabricate | third-party trademark | nbc, axios, bump-logo, finsmes, tc, glamour |
| advisor-portrait | must-not-fabricate | real likeness | lilly.png, kate.png |
| user-story-photo | must-not-fabricate | real likeness | meg, seb-and-daughter, naina |
| lifestyle-photo | must-not-fabricate | real likeness | FAQ portraits 2–6.png |
| blog-cover-photo | must-not-fabricate | licensed editorial | 3 blog cover jpegs |
| store-badge | must-not-fabricate | third-party trademark | App Store badge, Apple glyphs |
| app-store-onelink | must-not-reuse-live-endpoint | live endpoint | rileyapp.onelink.me links |
| newsletter-endpoint | must-not-reuse-live-endpoint | live endpoint | footer form (no real endpoint; submit prevented) |
| decorative-cloud | may-generate-new | generic | hero/faq/background clouds (no faces) |
| ui-icon | may-generate-new | generic | arrows, checks, stars, pictograms |
| internal-route | may-generate-new | generic | same-site links |
| unspecified-destination | may-generate-new | generic | CTAs whose destination is UNVERIFIED |

## Licensing rules (Riley is a real live company)

- **must-reuse-exact.** This is proprietary Riley IP. Only registered files are allowed, and
  only when `page.brandContext` is `riley-clone`. Output for any other brand must not
  reproduce or imitate the wordmark, the mascot characters, or the illustrations.
- **must-not-fabricate.** These carry real-world weight: real people, real trademarks and real
  articles. Never generate a substitute (no AI clinicians, customers, press logos or store
  badges). Use registered files only, and only in `riley-clone`.
- **must-not-reuse-live-endpoint.** PageSpecs carry the role, never the URL. Generated output
  must not embed Riley's live onelinks or wire the newsletter to any live endpoint.

## Enforcement

- **Pinned values.** The 14 non-generic roles are pinned to their policy in code
  (`schema/semantic_validate.py` `PINNED_POLICIES`). `extraction/verify_all.py` fails if the
  registry re-pins one, even to another valid policy value (proven by the adversarial and
  drift tests).
- **Registered refs.** `REGISTERED_ASSET_REF` rejects unregistered or `generated:` refs for
  reuse and no-fabricate roles.
- **Brand context.** `BRAND_CONTEXT_ASSET_POLICY` rejects restricted roles on `other-brand`
  pages.
- **File coverage.** Every file in the source `public/assets/` either has a role or a stated
  reason in `unassignedFiles`: four byte-identical duplicates, plus `blog/` (pending scope).
