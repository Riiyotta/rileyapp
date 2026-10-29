# Asset roles

`assets/asset-roles.json` is a closed enum of 31 roles derived from real usage sites (`usageSites`
cites) and wired through the schema (each media/link field allows only its own roles plus their generation-safe
substitutes), the allowlist and the examples. Media is `{assetRole, assetRef, alt?}`; links are
`{label, assetRole}`; only `placeholder-url` objects carry an `href`, on `.example` / `.invalid` hosts.

| role | availability | generationPolicy | generation-safe substitutes | weight |
|---|---|---|---|---|
| brand-wordmark | clone-only | must-reuse-exact | placeholder-brand-mark, user-supplied-asset | proprietary-brand-mark |
| mascot-illustration | clone-only | must-reuse-exact | generated-illustration, user-supplied-asset | proprietary-character-ip |
| mascot-family-mark | clone-only | must-reuse-exact | generated-illustration, user-supplied-asset | proprietary-character-ip |
| mascot-avatar | clone-only | must-reuse-exact | fictional-person-avatar, generated-illustration | proprietary-character-ip |
| brand-illustration | clone-only | must-reuse-exact | generated-illustration, user-supplied-asset | proprietary-artwork |
| rive-animation | clone-only | must-reuse-exact | placeholder-screenshot | proprietary-artwork |
| press-logo | blocked-for-generation | must-not-fabricate | placeholder-logo | third-party-trademark |
| advisor-portrait | blocked-for-generation | must-not-fabricate | fictional-person-avatar | real-person-likeness |
| user-story-photo | blocked-for-generation | must-not-fabricate | fictional-person-avatar, generated-illustration | real-person-likeness |
| lifestyle-photo | blocked-for-generation | must-not-fabricate | generated-illustration, user-supplied-asset | real-person-likeness |
| blog-cover-photo | blocked-for-generation | must-not-fabricate | generated-illustration, user-supplied-asset | licensed-editorial-photo |
| store-badge | blocked-for-generation | must-not-fabricate | user-supplied-asset | third-party-trademark |
| decorative-cloud | generation-safe | may-generate-new | - | generic-decoration |
| ui-icon | generation-safe | may-generate-new | - | generic-ui |
| app-store-onelink | blocked-for-generation | must-not-reuse-live-endpoint | placeholder-url | live-endpoint |
| newsletter-endpoint | blocked-for-generation | must-not-reuse-live-endpoint | placeholder-url | live-endpoint |
| internal-route | generation-safe | may-generate-new | - | generic-ui |
| unspecified-destination | generation-safe | may-generate-new | - | generic-ui |
| article-cover-photo | blocked-for-generation | must-not-fabricate | generated-illustration, user-supplied-asset | licensed-editorial-photo |
| author-avatar | blocked-for-generation | must-not-fabricate | fictional-person-avatar | real-person-likeness |
| social-share-mark | blocked-for-generation | must-not-fabricate | user-supplied-asset | third-party-trademark |
| policy-embed | blocked-for-generation | must-not-reuse-live-endpoint | placeholder-url | live-endpoint |
| source-citation | blocked-for-generation | must-not-fabricate | placeholder-url | health-claim-evidence |
| placeholder-brand-mark | generation-safe | may-generate-new | - | generation-safe-substitute |
| user-supplied-asset | generation-safe | may-generate-new | - | generation-safe-substitute |
| generated-illustration | generation-safe | may-generate-new | - | generation-safe-substitute |
| placeholder-screenshot | generation-safe | may-generate-new | - | generation-safe-substitute |
| fictional-person-avatar | generation-safe | may-generate-new | - | generation-safe-substitute |
| placeholder-logo | generation-safe | may-generate-new | - | generation-safe-substitute |
| placeholder-url | generation-safe | may-generate-new | - | generation-safe-substitute |
| original-copy | generation-safe | may-generate-new | - | generation-safe-substitute |

## Rules (Riley is a real, live company; much imagery shows real babies and parents)

- **clone-only** (Riley-owned IP: wordmark, mascots, illustrations, Rive screens): registered files, `mode: clone` only.
- **blocked-for-generation** (real people and children, third-party marks, App Store badge, live endpoints, policy
  embeds, health citations): registered files/endpoints in `mode: clone` only; never in `mode: generation`, never a
  substitute.
- **generation-safe**: usable in `mode: generation`, but only with `generated:`, `user-supplied:` or `placeholder:`
  refs — `/assets/...` files are Riley source files and are rejected there (`GENERATION_MODE_ASSET`).
- A real logo/wordmark is never `must-reuse-exact` in generation mode: `brand-wordmark` is `clone-only`, and the
  validators refuse a `must-reuse-exact` role that is `generation-safe`.

## Enforcement

- `PINNED_POLICIES` and `PINNED_AVAILABILITY` in `schema/semantic_validate.py`, re-pinned independently in
  `extraction/verify_all.py`; editing the registry alone (even to another valid value) fails (`prove_drift.py`).
- `REGISTERED_ASSET_REF` (clone), `GENERATION_MODE_*` (generation), `PLACEHOLDER_HREF_ROLE` (hrefs).
- Every file in the source `public/assets/` has a role or a stated reason in `unassignedFiles` (byte-identical
  duplicates and blog covers not referenced by any post).
