#!/usr/bin/env python3
"""Semantic validator for Riley-clone PageSpecs (pageSpecVersion 2.0.0).

Usage:
    python3 schema/semantic_validate.py                       # validates every schema/examples/*.pagespec.json
    python3 schema/semantic_validate.py a.json b.json         # validates the given PageSpecs

Runs (1) Draft-07 schema validation and (2) every rule in compatibility/graph.json. Each graph rule id has exactly
one implementation in RULE_IMPLS; the validator refuses to run if the id sets differ. Severity and exceptions are
read from graph.json at runtime, so prose and enforcement share one source of truth.

Modes (page.mode, required, closed):
  clone       faithful reconstruction of THIS Riley clone: real Riley assets / copy are allowed as evidence, but
              restricted roles must use their registered files.
  generation  a new page for another brand: GENERATION_MODE_* rules reject Riley brand, assets, real people,
              press/competitor names, copy (hashed 5-word shingles), health/development claims, ratings, URLs,
              policy embeds and store marks. Patterns live in schema/leakage-patterns.json, built from the real
              source by extraction/build_leakage_patterns.py. Detection is string-based (see the caveat there).

Pins kept IN CODE (independent of the registries, so editing a JSON file alone cannot loosen them):
  PINNED_POLICIES        generationPolicy of every real-world-weighted asset role
  PINNED_AVAILABILITY    availability of EVERY asset role (clone-only | generation-safe | blocked-for-generation)
  RETRIEVAL_INELIGIBLE   sections that are runtime UI (retrievalEligible:false); also re-pinned in verify_all.py

The repo root is derived from this file's location (no absolute paths). Exit code 0 = no error-severity findings.
"""
import glob
import json
import os
import re
import sys

from jsonschema import Draft7Validator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "schema"))
from textnorm import normalize, shingles  # noqa: E402
import hashlib  # noqa: E402

PINNED_POLICIES = {
    "brand-wordmark": "must-reuse-exact",
    "mascot-illustration": "must-reuse-exact",
    "mascot-family-mark": "must-reuse-exact",
    "mascot-avatar": "must-reuse-exact",
    "brand-illustration": "must-reuse-exact",
    "rive-animation": "must-reuse-exact",
    "press-logo": "must-not-fabricate",
    "advisor-portrait": "must-not-fabricate",
    "user-story-photo": "must-not-fabricate",
    "lifestyle-photo": "must-not-fabricate",
    "blog-cover-photo": "must-not-fabricate",
    "article-cover-photo": "must-not-fabricate",
    "author-avatar": "must-not-fabricate",
    "store-badge": "must-not-fabricate",
    "social-share-mark": "must-not-fabricate",
    "source-citation": "must-not-fabricate",
    "app-store-onelink": "must-not-reuse-live-endpoint",
    "newsletter-endpoint": "must-not-reuse-live-endpoint",
    "policy-embed": "must-not-reuse-live-endpoint",
}
PINNED_AVAILABILITY = {
    "brand-wordmark": "clone-only", "mascot-illustration": "clone-only", "mascot-family-mark": "clone-only",
    "mascot-avatar": "clone-only", "brand-illustration": "clone-only", "rive-animation": "clone-only",
    "press-logo": "blocked-for-generation", "advisor-portrait": "blocked-for-generation", "user-story-photo": "blocked-for-generation",
    "lifestyle-photo": "blocked-for-generation", "blog-cover-photo": "blocked-for-generation", "article-cover-photo": "blocked-for-generation",
    "author-avatar": "blocked-for-generation", "store-badge": "blocked-for-generation", "social-share-mark": "blocked-for-generation",
    "app-store-onelink": "blocked-for-generation", "newsletter-endpoint": "blocked-for-generation", "policy-embed": "blocked-for-generation",
    "source-citation": "blocked-for-generation",
    "decorative-cloud": "generation-safe", "ui-icon": "generation-safe", "internal-route": "generation-safe", "unspecified-destination": "generation-safe",
    "placeholder-brand-mark": "generation-safe", "user-supplied-asset": "generation-safe", "generated-illustration": "generation-safe",
    "placeholder-screenshot": "generation-safe", "fictional-person-avatar": "generation-safe", "placeholder-logo": "generation-safe",
    "placeholder-url": "generation-safe", "original-copy": "generation-safe",
}
AVAILABILITY_VALUES = {"clone-only", "generation-safe", "blocked-for-generation"}
RETRIEVAL_INELIGIBLE = {"cookie-consent"}
RUNTIME_UI_RX = re.compile(r"cookie|consent|modal|dialog|drawer|popup|pop-up|overlay|preloader|loader|toast|lightbox|tooltip", re.I)
RESTRICTED = {"must-reuse-exact", "must-not-fabricate", "must-not-reuse-live-endpoint"}
MARQUEE_PATTERNS = {"marquee-press-20s", "marquee-family-50s-reverse"}
GEN_REF_PREFIXES = ("generated:", "user-supplied:", "placeholder:")
PLACEHOLDER_HOST_RX = re.compile(r"^([a-z0-9-]+\.)*[a-z0-9-]+\.(example|invalid)$")
URL_RX = re.compile(r"(?:https?://|www\.)[^\s\"'<>)]+|\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|net|org|io|me|app|co|ai|dev|ly|link)\b(?:/[^\s\"'<>)]*)?", re.I)
# keys whose string values are identifiers/enums, not copy
NON_COPY_KEYS = {"type", "variant", "assetRole", "assetRef", "pattern", "reducedMotionFallback", "tone", "kind", "policy", "mode",
                 "theme", "template", "pageSpecVersion", "route", "href", "embedId", "surface", "text_token", "accent", "spacing",
                 "fontFamily", "radius", "artboard", "stateMachine"}
STYLE_PROPERTY_CATEGORIES = {"surface": {"color-roles"}, "text": {"color-roles"}, "accent": {"color-roles"},
                             "spacing": {"section-spacing"}, "fontFamily": {"font-family"}, "radius": {"radius"}}
RAW_COLOR_RX = re.compile(r"#[0-9a-f]{3,8}\b|\b(rgba?|hsla?|hwb|lab|lch|oklch|oklab|color)\s*\(", re.I)
RAW_LENGTH_RX = re.compile(r"^-?\d*\.?\d+\s*(px|rem|em|%|vh|vw|vmin|vmax|pt|ch|ex)?$|\d\s*(px|rem|em|vh|vw)\b", re.I)


def load(rel):
    with open(os.path.join(ROOT, rel)) as f:
        return json.load(f)


class Ctx:
    def __init__(self, schema=None, templates=None, graph=None, roles=None, sections=None, patterns=None, catalog=None):
        self.schema = schema or load("schema/pagespec.schema.json")
        self.templates = templates or load("templates/templates.json")
        self.graph = graph or load("compatibility/graph.json")
        self.roles = roles or load("assets/asset-roles.json")
        self.patterns = patterns or load("schema/leakage-patterns.json")
        self.catalog = catalog or load("tokens/llm/token-catalog.json")
        if sections is None:
            sections = {}
            for fn in sorted(glob.glob(os.path.join(ROOT, "sections", "*.json"))):
                with open(fn) as f:
                    d = json.load(f)
                sections[d["id"]] = d
        self.sections = sections
        self.rules = {r["id"]: r for r in self.graph["rules"]}
        self.route_map = {r["path"]: r for r in self.templates["routes"]}
        self.shingle_hashes = set(self.patterns["copyShingles"]["hashes"])
        c = re.compile
        P = self.patterns
        self.rx = {
            "brand": [(b["id"], c(b["regex"])) for b in P["brand"]],
            "person": [(p["name"], c(p["regex"])) for p in P["persons"]],
            "org": [(o["name"], c(o["regex"])) for o in P["organizations"]],
            "claim": [(x["id"], c(x["regex"])) for x in P["claims"]] + [("policy:" + r, c(r)) for r in P["policy"]["claims"]],
            "rating": [(x["id"], c(x["regex"])) for x in P["ratings"]] + [("policy:" + r, c(r)) for r in P["policy"]["ratings"]],
            "store": [(x["id"], c(x["regex"])) for x in P["storeMarks"]],
        }
        self.domains = [d["domain"] for d in P["domains"]]
        self.embed_ids = [normalize(e["id"]) for e in P["embedIds"]]
        self.asset_ids = [normalize(e["id"]) for e in P["assetIdentifiers"]]
        self.article_routes = {r["path"] for r in self.templates["routes"] if r["template"] == "blog-article"}


# ---------------------------------------------------------------- helpers
def words(s):
    return len(s.split())


def node_def(ctx, node, overlay=False):
    defs = ctx.schema["definitions"]
    t, v = node.get("type"), node.get("variant")
    if v is not None and f"node_{t}__{v}" in defs:
        return defs[f"node_{t}__{v}"]
    return defs.get(f"node_{t}")


def walk_maxwords(sch, inst, path, out):
    if isinstance(inst, str) and "x-maxWords" in sch:
        n = words(inst)
        if n > sch["x-maxWords"]:
            out.append(f"{path}: {n} words > maxWords {sch['x-maxWords']}")
    elif isinstance(inst, dict) and sch.get("type") == "object":
        for k, v in inst.items():
            if k in sch.get("properties", {}):
                walk_maxwords(sch["properties"][k], v, f"{path}.{k}", out)
    elif isinstance(inst, list) and sch.get("type") == "array":
        for i, v in enumerate(inst):
            walk_maxwords(sch["items"], v, f"{path}[{i}]", out)


def iter_role_objects(obj, path):
    if isinstance(obj, dict):
        if "assetRole" in obj:
            yield path, obj
        for k, v in obj.items():
            yield from iter_role_objects(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_role_objects(v, f"{path}[{i}]")


def iter_strings(obj, path, key=None):
    """Yield (path, key, string) for every string leaf."""
    if isinstance(obj, str):
        yield path, key, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(v, f"{path}.{k}", k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, f"{path}[{i}]", key)


def copy_strings(spec):
    """Every copy string of the page (page title/brand + nodes + overlays), excluding identifier/enum fields."""
    out = []
    for root, val in (("page", spec.get("page", {})), ("nodes", spec.get("nodes", [])), ("overlays", spec.get("overlays", []))):
        for p, k, s in iter_strings(val, root):
            if k in NON_COPY_KEYS or p.startswith("page.route") or p.endswith(".style") or ".style." in p:
                continue
            out.append((p, s))
    return out


def all_nodes(spec):
    return list(spec.get("nodes", [])) + list(spec.get("overlays", []))


def is_generation(spec):
    return spec.get("page", {}).get("mode") == "generation"


def key(node):
    return (node.get("type"), node.get("variant"))


def _types(spec):
    return [n.get("type") for n in spec["nodes"]]


# ---------------------------------------------------------------- structural rules
def rule_template_node_sequence(ctx, spec):
    out = []
    tname = spec["page"]["template"]
    tnodes = ctx.templates["templates"][tname]["nodes"]
    nodes = spec["nodes"]
    i = 0
    for tn in tnodes:
        def matches(n):
            return n.get("type") == tn["section"] and ("variant" not in tn or n.get("variant") == tn["variant"])
        count = 0
        while i < len(nodes) and matches(nodes[i]) and (tn["repeatable"] or count == 0):
            i += 1
            count += 1
        if count == 0 and tn["required"]:
            want = tn["section"] + (f"[{tn['variant']}]" if "variant" in tn else "")
            got = nodes[i].get("type") + (f"[{nodes[i].get('variant')}]" if nodes[i].get("variant") else "") if i < len(nodes) else "end of nodes"
            out.append(f"template '{tname}' requires {want} at position {i}, found {got}")
            return out
    if i < len(nodes):
        out.append(f"template '{tname}': unexpected extra/out-of-order node at position {i}: {nodes[i].get('type')}")
    return out


def rule_one_per_page(ctx, spec):
    seen, out = {}, []
    for i, n in enumerate(spec["nodes"]):
        t = n.get("type")
        if ctx.sections.get(t, {}).get("constraints", {}).get("onePerPage"):
            if t in seen:
                out.append(f"{t} appears more than once (positions {seen[t]} and {i})")
            seen.setdefault(t, i)
    return out


def rule_announcement_first(ctx, spec):
    t = _types(spec)
    if "announcement-bar" in t and t.index("announcement-bar") != 0:
        return [f"announcement-bar must be node 0, found at {t.index('announcement-bar')}"]
    return []


def rule_header_after_announcement(ctx, spec):
    t = _types(spec)
    if "site-header" not in t:
        return []
    want = 1 if t and t[0] == "announcement-bar" else 0
    if t.index("site-header") != want:
        return [f"site-header must be node {want} ({'right after announcement-bar' if want else 'first: no announcement-bar'}), found at {t.index('site-header')}"]
    return []


def rule_footer_last(ctx, spec):
    t = _types(spec)
    if "site-footer" in t and t.index("site-footer") != len(t) - 1:
        return [f"site-footer must be the last node, found at {t.index('site-footer')} of {len(t)}"]
    return []


def rule_header_variant_binding(ctx, spec):
    out, nodes = [], spec["nodes"]
    for i, n in enumerate(nodes):
        if n.get("type") == "site-header":
            nxt = nodes[i + 1].get("type") if i + 1 < len(nodes) else None
            want = "hero-overlay" if nxt == "hero-home" else "standalone"
            if n.get("variant") != want:
                out.append(f"site-header variant must be '{want}' when followed by {nxt}, got '{n.get('variant')}'")
    return out


def rule_press_follows_hero(ctx, spec):
    t = _types(spec)
    return ["press-marquee must immediately follow hero-home" for i, x in enumerate(t) if x == "press-marquee" and (i == 0 or t[i - 1] != "hero-home")]


def rule_one_hero(ctx, spec):
    exempt = {e["template"] for e in ctx.rules["ONE_HERO"]["exceptions"]}
    if spec["page"]["template"] in exempt:
        return []
    cats = ctx.graph["categories"]
    heroes = [t for t in _types(spec) if cats.get(t) == "hero"]
    return [] if len(heroes) == 1 else [f"expected exactly 1 hero section, found {len(heroes)}: {heroes}"]


def rule_final_cta_precedes_footer(ctx, spec):
    t = _types(spec)
    if "final-cta" in t:
        i = t.index("final-cta")
        if i + 1 >= len(t) or t[i + 1] != "site-footer":
            return ["final-cta must immediately precede site-footer"]
    return []


def rule_no_adjacent_carousels(ctx, spec):
    t, pair = _types(spec), {"featurette-carousel", "testimonials-carousel"}
    return [f"{a} adjacent to {b}" for a, b in zip(t, t[1:]) if {a, b} == pair]


def rule_adjacent_marquees(ctx, spec):
    allowed = {tuple(e["pair"]) for e in ctx.rules["ADJACENT_MARQUEES"]["exceptions"]}
    out, nodes = [], spec["nodes"]
    for a, b in zip(nodes, nodes[1:]):
        pa, pb = a.get("motion", {}).get("pattern"), b.get("motion", {}).get("pattern")
        if pa in MARQUEE_PATTERNS and pb in MARQUEE_PATTERNS and (a["type"], b["type"]) not in allowed:
            out.append(f"adjacent marquees {a['type']} -> {b['type']}")
    return out


def rule_motion_budget(ctx, spec):
    n = sum(1 for x in spec["nodes"] if x.get("motion", {}).get("pattern") in MARQUEE_PATTERNS)
    return [f"{n} infinite marquee sections (budget 2)"] if n > 2 else []


def rule_route_template_binding(ctx, spec):
    route, tpl = spec["page"]["route"], spec["page"]["template"]
    r = ctx.route_map.get(route)
    if r and r["template"] != tpl:
        extra = " (dead sitemap slug / unbuilt link: only the not-found template is allowed)" if r.get("deadSlug") or r.get("unbuiltLink") else ""
        return [f"route {route} is mapped to template '{r['template']}', PageSpec declares '{tpl}'{extra}"]
    return []


def rule_max_words(ctx, spec):
    out = []
    for coll in ("nodes", "overlays"):
        for i, n in enumerate(spec.get(coll, [])):
            d = node_def(ctx, n)
            if d:
                walk_maxwords(d["properties"]["content"], n.get("content", {}), f"{coll}[{i}]({n.get('type')}).content", out)
    walk_maxwords(ctx.schema["properties"]["page"], spec.get("page", {}), "page", out)
    return out


def rule_comparison_matrix_shape(ctx, spec):
    out = []
    for i, n in enumerate(spec["nodes"]):
        ct = n.get("content", {}).get("comparisonTable") if n.get("type") == "gradient-band" else None
        if ct:
            nc = len(ct.get("columns", []))
            for j, r in enumerate(ct.get("rows", [])):
                if len(r.get("marks", [])) != nc:
                    out.append(f"nodes[{i}] comparison row {j} has {len(r['marks'])} marks for {nc} columns")
    return out


def rule_reduced_motion_fallback(ctx, spec):
    out = []
    for i, n in enumerate(all_nodes(spec)):
        m = n.get("motion")
        if not isinstance(m, dict) or not m.get("reducedMotionFallback"):
            out.append(f"node {i} ({n.get('type')}) motion lacks reducedMotionFallback")
    return out


def rule_pagination_bounds(ctx, spec):
    out = []
    for i, n in enumerate(spec["nodes"]):
        if n.get("type") == "blog-pagination":
            c = n["content"]
            if c["page"] > c["totalPages"]:
                out.append(f"nodes[{i}] page {c['page']} > totalPages {c['totalPages']}")
            if spec["page"]["template"] == "blog-category" and c["totalPages"] != 1:
                out.append(f"nodes[{i}] blog-category always renders 'Page 1 of 1' (measured), got totalPages {c['totalPages']}")
        if n.get("type") == "blog-category-tabs":
            c = n["content"]
            if c["activeIndex"] >= len(c["tabs"]):
                out.append(f"nodes[{i}] activeIndex {c['activeIndex']} has no tab")
    return out


BLOCK_NEEDS = {"list": "items", "promo": "cta", "image": "image", "downloadable-image": "image"}


def rule_article_block_shape(ctx, spec):
    out = []
    for i, n in enumerate(spec["nodes"]):
        for j, b in enumerate(n.get("content", {}).get("blocks", []) if n.get("type") in ("article-intro", "article-chapter") else []):
            need = BLOCK_NEEDS.get(b["kind"])
            if need and need not in b:
                out.append(f"nodes[{i}].blocks[{j}] kind '{b['kind']}' needs '{need}'")
            for extra in ("items", "cta", "image"):
                if extra in b and BLOCK_NEEDS.get(b["kind"]) != extra:
                    out.append(f"nodes[{i}].blocks[{j}] kind '{b['kind']}' must not carry '{extra}'")
    return out


def rule_article_citations_resolve(ctx, spec):
    src = next((n for n in spec["nodes"] if n.get("type") == "article-sources"), None)
    if src is None:
        return []
    have = len(src["content"].get("sources", []))
    out = []
    for i, n in enumerate(spec["nodes"]):
        for j, b in enumerate(n.get("content", {}).get("blocks", []) if n.get("type") in ("article-intro", "article-chapter") else []):
            for c in b.get("citations", []):
                if c > have:
                    out.append(f"nodes[{i}].blocks[{j}] cites source {c} but article-sources lists {have}")
    return out


def rule_toc_matches_chapters(ctx, spec):
    toc = next((n for n in spec["nodes"] if n.get("type") == "article-toc"), None)
    if toc is None:
        return []
    heads = [n["content"]["heading"] for n in spec["nodes"] if n.get("type") == "article-chapter"]
    entries = [e["label"] for e in toc["content"]["entries"]]
    return [] if entries == heads else [f"article-toc entries {entries} must equal the article-chapter headings in order {heads}"]


def rule_retrieval_ineligible_node(ctx, spec):
    out = []
    for i, n in enumerate(spec["nodes"]):
        t = n.get("type")
        if t in RETRIEVAL_INELIGIBLE or ctx.sections.get(t, {}).get("retrievalEligible") is False:
            out.append(f"nodes[{i}] {t} is runtime UI (retrievalEligible:false) and may only appear in overlays[]")
    for i, n in enumerate(spec.get("overlays", [])):
        t = n.get("type")
        if t not in RETRIEVAL_INELIGIBLE or ctx.sections.get(t, {}).get("retrievalEligible") is not False:
            out.append(f"overlays[{i}] {t} is not a pinned retrieval-ineligible overlay")
    return out


def rule_placeholder_href_role(ctx, spec):
    out = []
    for path, o in iter_role_objects(all_nodes(spec), "nodes"):
        if "href" in o and o["assetRole"] != "placeholder-url":
            out.append(f"{path}: href is only allowed with assetRole placeholder-url (got {o['assetRole']})")
        if o["assetRole"] == "placeholder-url" and "href" not in o:
            out.append(f"{path}: assetRole placeholder-url needs an href on a .example/.invalid host")
    return out


def rule_registered_asset_ref(ctx, spec):
    out = []
    for path, o in iter_role_objects(all_nodes(spec), "nodes"):
        if "assetRef" not in o:
            continue
        role = ctx.roles["roles"].get(o["assetRole"])
        if not role:
            continue
        ref, pol = o["assetRef"], role["generationPolicy"]
        if ref.startswith(GEN_REF_PREFIXES):
            if pol != "may-generate-new":
                out.append(f"{path}: non-source ref {ref} not allowed for role '{o['assetRole']}' ({pol})")
        elif pol in ("must-reuse-exact", "must-not-fabricate") and ref not in role.get("files", []):
            out.append(f"{path}: assetRef {ref} is not a registered file of role '{o['assetRole']}' ({pol})")
        elif ref.startswith("/assets/") and pol == "may-generate-new" and role.get("files") is not None and ref not in role["files"]:
            out.append(f"{path}: assetRef {ref} is not a registered source file of role '{o['assetRole']}'")
    return out


# ---------------------------------------------------------------- generation-mode leakage rules
WEIGHT_RULE = {
    "real-person-likeness": "GENERATION_MODE_PERSON",
    "third-party-trademark": "GENERATION_MODE_CUSTOMER",
    "live-endpoint": "GENERATION_MODE_URL",
    "health-claim-evidence": "GENERATION_MODE_CLAIM",
}
ROLE_RULE = {"rive-animation": "GENERATION_MODE_SCREENSHOT", "store-badge": "GENERATION_MODE_STORE", "app-store-onelink": "GENERATION_MODE_STORE",
             "policy-embed": "GENERATION_MODE_EMBED", "social-share-mark": "GENERATION_MODE_CUSTOMER"}


def _asset_findings(ctx, spec):
    """(rule_id, message) for every generation-mode asset violation, routed to the most specific rule."""
    res = []
    if not is_generation(spec):
        return res
    for path, o in iter_role_objects(all_nodes(spec), "nodes"):
        r = o["assetRole"]
        avail = PINNED_AVAILABILITY.get(r) or ctx.roles["roles"].get(r, {}).get("availability")
        if avail != "generation-safe":
            weight = ctx.roles["roles"].get(r, {}).get("weight")
            rid = ROLE_RULE.get(r) or WEIGHT_RULE.get(weight) or "GENERATION_MODE_ASSET"
            subs = ctx.roles["roles"].get(r, {}).get("generationSafeSubstitutes", [])
            res.append((rid, f"{path}: assetRole '{r}' is {avail} (use one of {subs})"))
            if rid != "GENERATION_MODE_ASSET":
                res.append(("GENERATION_MODE_ASSET", f"{path}: assetRole '{r}' is {avail}"))
        ref = o.get("assetRef")
        if isinstance(ref, str) and not ref.startswith(GEN_REF_PREFIXES):
            res.append(("GENERATION_MODE_ASSET", f"{path}: assetRef {ref} is a Riley source file (generation mode needs generated:/user-supplied:/placeholder:)"))
    for p, s in copy_strings(spec):
        ns = normalize(s)
        for aid in ctx.asset_ids:
            if aid in ns:
                res.append(("GENERATION_MODE_SCREENSHOT", f"{p}: Riley Rive asset identifier '{aid}'"))
    for p, k, s in iter_strings(all_nodes(spec), "nodes"):
        if k in ("artboard", "stateMachine") and normalize(s) in ctx.asset_ids:
            res.append(("GENERATION_MODE_SCREENSHOT", f"{p}: Riley Rive asset identifier '{s}'"))
    return res


def _asset_rule(rid):
    def f(ctx, spec):
        return [m for r, m in _asset_findings(ctx, spec) if r == rid]
    f.__name__ = f"rule_{rid.lower()}_assets"
    return f


def _scan(ctx, spec, family, label):
    if not is_generation(spec):
        return []
    out = []
    for p, s in copy_strings(spec):
        ns = normalize(s)
        for name, rx in ctx.rx[family]:
            if rx.search(ns):
                out.append(f"{p}: {label} '{name}' in {s[:70]!r}")
    return out


def rule_generation_mode_brand(ctx, spec):
    page = spec.get("page", {})
    if not is_generation(spec):
        return ["page.brand is only for generation mode (clone mode renders Riley itself)"] if "brand" in page else []
    out = [] if "brand" in page else ["generation mode requires page.brand (the fictional/operator brand being generated for)"]
    out += _scan(ctx, spec, "brand", "Riley brand/product mark")
    for p, k, s in iter_strings(spec.get("page", {}), "page"):
        if k == "route" and re.search(r"riley", normalize(s)):
            out.append(f"{p}: Riley brand in route {s}")
    return out


def rule_generation_mode_person(ctx, spec):
    return _scan(ctx, spec, "person", "real person") + _asset_rule("GENERATION_MODE_PERSON")(ctx, spec)


def rule_generation_mode_customer(ctx, spec):
    return _scan(ctx, spec, "org", "real press/partner/competitor") + _asset_rule("GENERATION_MODE_CUSTOMER")(ctx, spec)


def rule_generation_mode_claim(ctx, spec):
    return _scan(ctx, spec, "claim", "health/development/pricing claim") + _asset_rule("GENERATION_MODE_CLAIM")(ctx, spec)


def rule_generation_mode_rating(ctx, spec):
    return _scan(ctx, spec, "rating", "review/rating")


def rule_generation_mode_store(ctx, spec):
    return _scan(ctx, spec, "store", "app-store mark/link") + _asset_rule("GENERATION_MODE_STORE")(ctx, spec)


def rule_generation_mode_copy(ctx, spec):
    if not is_generation(spec):
        return []
    out = []
    for p, s in copy_strings(spec):
        hits = [sh for sh in shingles(s, 5) if hashlib.sha256(sh.encode()).hexdigest()[:16] in ctx.shingle_hashes]
        if hits:
            out.append(f"{p}: {len(hits)} 5-word shingle(s) match Riley source copy, e.g. {hits[0]!r}")
    return out


def rule_generation_mode_url(ctx, spec):
    if not is_generation(spec):
        return []
    out = []
    route = spec["page"].get("route", "")
    if route in ctx.article_routes:
        out.append(f"page.route {route} is a Riley article URL")
    for p, k, s in iter_strings({"page": spec.get("page", {}), "nodes": all_nodes(spec)}, ""):
        if k in ("assetRole", "assetRef", "type", "pattern", "reducedMotionFallback"):
            continue
        ns = normalize(s)
        for d in ctx.domains:
            if d in ns:
                out.append(f"{p}: Riley/source domain '{d}'")
        for m in URL_RX.finditer(ns):
            u = m.group(0)
            host = re.sub(r"^(https?://)?(www\.)?", "", u).split("/")[0].split(":")[0]
            if not PLACEHOLDER_HOST_RX.match(host):
                out.append(f"{p}: URL host '{host}' is not a reserved .example/.invalid placeholder")
    return out + _asset_rule("GENERATION_MODE_URL")(ctx, spec)


def rule_generation_mode_embed(ctx, spec):
    if not is_generation(spec):
        return []
    out = []
    for p, k, s in iter_strings({"nodes": all_nodes(spec), "page": spec.get("page", {})}, ""):
        ns = normalize(s)
        for e in ctx.embed_ids:
            if e in ns:
                out.append(f"{p}: Riley policy-embed id/vendor '{e}'")
    return out + _asset_rule("GENERATION_MODE_EMBED")(ctx, spec)


def rule_generation_mode_screenshot(ctx, spec):
    return _asset_rule("GENERATION_MODE_SCREENSHOT")(ctx, spec)


def rule_generation_mode_asset(ctx, spec):
    return _asset_rule("GENERATION_MODE_ASSET")(ctx, spec)


# ---------------------------------------------------------------- token rules (node.style)
def _style_items(spec):
    for coll in ("nodes", "overlays"):
        for i, n in enumerate(spec.get(coll, [])):
            for prop, val in (n.get("style") or {}).items():
                yield f"{coll}[{i}]({n.get('type')}).style.{prop}", prop, val


def _is_token_path(val):
    return val.startswith("tokens.")


def rule_token_raw_color(ctx, spec):
    return [f"{p}: raw colour value {v!r}; use a tokens.10-semantic.color-roles path" for p, prop, v in _style_items(spec) if RAW_COLOR_RX.search(v)]


def rule_token_arbitrary_spacing(ctx, spec):
    return [f"{p}: arbitrary length {v!r}; use a catalog token" for p, prop, v in _style_items(spec)
            if not RAW_COLOR_RX.search(v) and not _is_token_path(v) and RAW_LENGTH_RX.search(v)]


def rule_token_unsupported_font(ctx, spec):
    fams = set(ctx.catalog["fontFamilies"])
    out = []
    for p, prop, v in _style_items(spec):
        if prop == "fontFamily" and v not in fams:
            out.append(f"{p}: font {v!r} is not a catalog font family {sorted(fams)}")
    return out


def rule_token_unknown(ctx, spec):
    toks = ctx.catalog["tokens"]
    out = []
    for p, prop, v in _style_items(spec):
        if RAW_COLOR_RX.search(v) or (not _is_token_path(v) and RAW_LENGTH_RX.search(v)) or prop == "fontFamily":
            continue  # reported by the more specific TOKEN_* rule
        if v not in toks:
            out.append(f"{p}: unknown token {v!r} (not in tokens/llm/token-catalog.json)")
    return out


def rule_token_theme_combination(ctx, spec):
    toks = ctx.catalog["tokens"]
    theme = spec["page"].get("theme")
    roles_in_theme = set(ctx.catalog["themes"].get(theme, []))
    out = []
    for p, prop, v in _style_items(spec):
        if v not in toks:
            if re.match(r"^tokens\.themes\.", v) and not v.startswith(f"tokens.themes.{theme}."):
                out.append(f"{p}: token {v!r} belongs to a different theme than page.theme '{theme}'")
            continue
        cat = toks[v]["category"]
        if cat not in STYLE_PROPERTY_CATEGORIES[prop]:
            out.append(f"{p}: {cat} token {v!r} is invalid for style.{prop} (needs {sorted(STYLE_PROPERTY_CATEGORIES[prop])})")
        if cat == "color-roles":
            role = v.split("tokens.10-semantic.color-roles.roles.", 1)[-1]
            if role not in roles_in_theme:
                out.append(f"{p}: colour role '{role}' is not defined in theme '{theme}'")
    return out


# ---------------------------------------------------------------- registry-level
def check_asset_roles(roles_doc, schema):
    """Registry-level: pinned policies + pinned availability + substitutes + closure against the schema enums."""
    out = []
    roles = roles_doc["roles"]
    for r, pol in PINNED_POLICIES.items():
        if r not in roles:
            out.append(f"pinned role '{r}' missing from asset-roles.json")
        elif roles[r]["generationPolicy"] != pol:
            out.append(f"role '{r}' is pinned to '{pol}' but asset-roles.json says '{roles[r]['generationPolicy']}'")
    if set(PINNED_AVAILABILITY) != set(roles):
        out.append(f"PINNED_AVAILABILITY and asset-roles.json disagree on the role set: {sorted(set(PINNED_AVAILABILITY) ^ set(roles))}")
    for r, d in roles.items():
        av = d.get("availability")
        if av not in AVAILABILITY_VALUES:
            out.append(f"role '{r}' has availability {av!r} (closed set {sorted(AVAILABILITY_VALUES)})")
        elif PINNED_AVAILABILITY.get(r) and av != PINNED_AVAILABILITY[r]:
            out.append(f"role '{r}' availability is pinned to '{PINNED_AVAILABILITY[r]}' but asset-roles.json says '{av}'")
        subs = d.get("generationSafeSubstitutes")
        if not isinstance(subs, list) or not isinstance(d.get("generatedModeGuidance"), str):
            out.append(f"role '{r}' needs generationSafeSubstitutes[] and generatedModeGuidance")
            continue
        if av != "generation-safe" and not subs:
            out.append(f"role '{r}' is {av} but declares no generationSafeSubstitutes")
        for s in subs:
            if PINNED_AVAILABILITY.get(s) != "generation-safe":
                out.append(f"role '{r}' substitute '{s}' is not a pinned generation-safe role")
        if d["generationPolicy"] == "must-reuse-exact" and av == "generation-safe":
            out.append(f"role '{r}' is must-reuse-exact but generation-safe: a real Riley mark can never be reused in generation mode")
    allowed = set(roles_doc["generationPolicies"])
    for r, d in roles.items():
        if d["generationPolicy"] not in allowed:
            out.append(f"role '{r}' has unknown generationPolicy '{d['generationPolicy']}'")
    used = set()

    def collect(o):
        if isinstance(o, dict):
            ar = o.get("properties", {}).get("assetRole") if o.get("type") == "object" else None
            if isinstance(ar, dict) and "enum" in ar:
                used.update(ar["enum"])
            for v in o.values():
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)
    collect(schema)
    missing = set(roles) - used - {"original-copy"}
    if used - set(roles) or missing:
        out.append(f"schema assetRole enums and asset-roles.json differ: {sorted((used - set(roles)) | missing)}")
    return out


def check_retrieval(sections):
    """Contract-level R8 pin: retrievalEligible false exactly for the pinned runtime-UI sections."""
    out = []
    for sid, d in sections.items():
        re_ = d.get("retrievalEligible")
        if not isinstance(re_, bool):
            out.append(f"section {sid}: retrievalEligible must be a boolean")
            continue
        pinned = sid in RETRIEVAL_INELIGIBLE
        if pinned and re_:
            out.append(f"section {sid} is pinned retrieval-ineligible (runtime UI) but its contract says retrievalEligible:true")
        if not pinned and not re_:
            out.append(f"section {sid} is retrievalEligible:false but not in the RETRIEVAL_INELIGIBLE pin (content sections stay eligible)")
        if not re_ and len(d.get("retrievalReason", "")) < 30:
            out.append(f"section {sid}: retrievalEligible:false needs a retrievalReason of 30+ characters")
        if RUNTIME_UI_RX.search(sid + " " + d.get("purpose", "")[:40]) and not pinned:
            out.append(f"section {sid} looks like runtime UI by id/title but is not pinned retrieval-ineligible")
    for sid in RETRIEVAL_INELIGIBLE - set(sections):
        out.append(f"pinned retrieval-ineligible section {sid} has no contract")
    return out


def rule_asset_role_pinning(ctx, spec):
    return check_asset_roles(ctx.roles, ctx.schema)


def rule_retrieval_contract_pin(ctx, spec):
    return check_retrieval(ctx.sections)


RULE_IMPLS = {
    "TEMPLATE_NODE_SEQUENCE": rule_template_node_sequence,
    "ONE_PER_PAGE": rule_one_per_page,
    "ANNOUNCEMENT_FIRST": rule_announcement_first,
    "HEADER_AFTER_ANNOUNCEMENT": rule_header_after_announcement,
    "FOOTER_LAST": rule_footer_last,
    "HEADER_VARIANT_BINDING": rule_header_variant_binding,
    "PRESS_FOLLOWS_HERO": rule_press_follows_hero,
    "ONE_HERO": rule_one_hero,
    "FINAL_CTA_PRECEDES_FOOTER": rule_final_cta_precedes_footer,
    "NO_ADJACENT_CAROUSELS": rule_no_adjacent_carousels,
    "ADJACENT_MARQUEES": rule_adjacent_marquees,
    "MOTION_BUDGET_INFINITE_LOOPS": rule_motion_budget,
    "ROUTE_TEMPLATE_BINDING": rule_route_template_binding,
    "REGISTERED_ASSET_REF": rule_registered_asset_ref,
    "PLACEHOLDER_HREF_ROLE": rule_placeholder_href_role,
    "MAX_WORDS": rule_max_words,
    "COMPARISON_MATRIX_SHAPE": rule_comparison_matrix_shape,
    "REDUCED_MOTION_FALLBACK": rule_reduced_motion_fallback,
    "PAGINATION_BOUNDS": rule_pagination_bounds,
    "ARTICLE_BLOCK_SHAPE": rule_article_block_shape,
    "ARTICLE_CITATIONS_RESOLVE": rule_article_citations_resolve,
    "TOC_MATCHES_CHAPTERS": rule_toc_matches_chapters,
    "RETRIEVAL_INELIGIBLE_NODE": rule_retrieval_ineligible_node,
    "RETRIEVAL_CONTRACT_PIN": rule_retrieval_contract_pin,
    "ASSET_ROLE_PINNING": rule_asset_role_pinning,
    "GENERATION_MODE_BRAND": rule_generation_mode_brand,
    "GENERATION_MODE_ASSET": rule_generation_mode_asset,
    "GENERATION_MODE_PERSON": rule_generation_mode_person,
    "GENERATION_MODE_CUSTOMER": rule_generation_mode_customer,
    "GENERATION_MODE_SCREENSHOT": rule_generation_mode_screenshot,
    "GENERATION_MODE_COPY": rule_generation_mode_copy,
    "GENERATION_MODE_CLAIM": rule_generation_mode_claim,
    "GENERATION_MODE_RATING": rule_generation_mode_rating,
    "GENERATION_MODE_STORE": rule_generation_mode_store,
    "GENERATION_MODE_URL": rule_generation_mode_url,
    "GENERATION_MODE_EMBED": rule_generation_mode_embed,
    "TOKEN_UNKNOWN": rule_token_unknown,
    "TOKEN_RAW_COLOR": rule_token_raw_color,
    "TOKEN_ARBITRARY_SPACING": rule_token_arbitrary_spacing,
    "TOKEN_UNSUPPORTED_FONT": rule_token_unsupported_font,
    "TOKEN_THEME_COMBINATION": rule_token_theme_combination,
}


def validate(spec, ctx=None):
    """Return (errors, warnings) as lists of strings."""
    ctx = ctx or Ctx()
    gids, impl = set(ctx.rules), set(RULE_IMPLS)
    if gids != impl:
        return [f"GRAPH/VALIDATOR DISAGREEMENT: graph-only {sorted(gids - impl)}, validator-only {sorted(impl - gids)}"], []
    errors, warns = [], []
    for e in Draft7Validator(ctx.schema).iter_errors(spec):
        errors.append(f"SCHEMA {list(e.absolute_path)}: {e.message[:160]}")
    if errors:
        return errors, warns  # semantic rules assume a schema-valid shape
    for rid, fn in RULE_IMPLS.items():
        for msg in fn(ctx, spec):
            (errors if ctx.rules[rid]["severity"] == "error" else warns).append(f"{rid}: {msg}")
    return errors, warns


def example_paths():
    return sorted(glob.glob(os.path.join(ROOT, "schema", "examples", "*.pagespec.json")))


def main(argv):
    paths = argv or example_paths()
    ctx, bad = Ctx(), 0
    for p in paths:
        with open(p) as f:
            spec = json.load(f)
        errors, warns = validate(spec, ctx)
        print(f"{os.path.basename(p)} [{spec.get('page', {}).get('mode')}/{spec.get('page', {}).get('template')}]: {len(errors)} error(s), {len(warns)} warning(s)")
        for e in errors:
            print("  ERROR", e)
        for w in warns:
            print("  WARN ", w)
        bad += bool(errors)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
