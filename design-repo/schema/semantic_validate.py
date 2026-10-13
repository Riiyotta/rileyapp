#!/usr/bin/env python3
"""Semantic validator for Riley-clone PageSpecs.

Usage:
    python3 schema/semantic_validate.py                 # validates schema/example.pagespec.json
    python3 schema/semantic_validate.py a.json b.json   # validates the given PageSpecs

Runs (1) Draft-07 schema validation and (2) every rule in compatibility/graph.json.
Each graph rule id has exactly one implementation in RULE_IMPLS; the validator refuses
to run if the id sets differ. Rule severity and exceptions are read from graph.json at
runtime, so the prose and the enforcement share one source of truth.

The repo root is derived from this file's location (no absolute paths).
Exit code 0 = no error-severity findings.
"""
import json
import os
import re
import sys

from jsonschema import Draft7Validator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Real-world-weighted asset roles are PINNED here, in code, independently of
# assets/asset-roles.json, so a re-pin of the registry (even to another valid
# policy value) is caught. Generic roles (decorative-cloud, ui-icon,
# internal-route, unspecified-destination) are intentionally not pinned.
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
    "store-badge": "must-not-fabricate",
    "app-store-onelink": "must-not-reuse-live-endpoint",
    "newsletter-endpoint": "must-not-reuse-live-endpoint",
}
RESTRICTED = {"must-reuse-exact", "must-not-fabricate", "must-not-reuse-live-endpoint"}
MARQUEE_PATTERNS = {"marquee-press-20s", "marquee-family-50s-reverse"}


def load(rel):
    with open(os.path.join(ROOT, rel)) as f:
        return json.load(f)


class Ctx:
    def __init__(self, schema=None, templates=None, graph=None, roles=None, sections=None):
        self.schema = schema or load("schema/pagespec.schema.json")
        self.templates = templates or load("templates/templates.json")
        self.graph = graph or load("compatibility/graph.json")
        self.roles = roles or load("assets/asset-roles.json")
        if sections is None:
            sections = {}
            sdir = os.path.join(ROOT, "sections")
            for fn in sorted(os.listdir(sdir)):
                if fn.endswith(".json"):
                    with open(os.path.join(sdir, fn)) as f:
                        d = json.load(f)
                    sections[d["id"]] = d
        self.sections = sections
        self.rules = {r["id"]: r for r in self.graph["rules"]}


# ---------------------------------------------------------------- helpers
def words(s):
    return len(s.split())


def node_def(ctx, node):
    """Return the schema definition matching this node's (type, variant)."""
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
    """Yield (path, dict) for every dict carrying an assetRole."""
    if isinstance(obj, dict):
        if "assetRole" in obj:
            yield path, obj
        for k, v in obj.items():
            yield from iter_role_objects(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_role_objects(v, f"{path}[{i}]")


def key(node):
    return (node.get("type"), node.get("variant"))


def excluded_match(route, patterns):
    for p in patterns:
        rx = "^" + re.sub(r"\\\{[^}]+\\\}", "[^/]+", re.escape(p)) + "$"
        if re.match(rx, route):
            return p
    return None


# ---------------------------------------------------------------- rules (one per graph id)
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


def _types(spec):
    return [n.get("type") for n in spec["nodes"]]


def rule_announcement_first(ctx, spec):
    t = _types(spec)
    if "announcement-bar" in t and t.index("announcement-bar") != 0:
        return [f"announcement-bar must be node 0, found at {t.index('announcement-bar')}"]
    return []


def rule_header_second(ctx, spec):
    t = _types(spec)
    if "site-header" in t and t.index("site-header") != 1:
        return [f"site-header must be node 1, found at {t.index('site-header')}"]
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
    out = []
    for i, x in enumerate(t):
        if x == "press-marquee" and (i == 0 or t[i - 1] != "hero-home"):
            out.append("press-marquee must immediately follow hero-home")
    return out


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
    for r in ctx.templates["routes"]:
        if r["path"] == route:
            if r["template"] != tpl:
                extra = " (dead sitemap slug: only the not-found template is allowed)" if r.get("deadSlug") else ""
                return [f"route {route} is mapped to template '{r['template']}', PageSpec declares '{tpl}'{extra}"]
            return []
    pats = [e["pattern"] for e in ctx.templates["excludedRoutes"]["routes"]]
    hit = excluded_match(route, pats)
    if hit:
        return [f"route {route} matches excluded/pending route '{hit}' — no template exists for it in this snapshot"]
    return []


def rule_brand_context_asset_policy(ctx, spec):
    if spec["page"].get("brandContext") != "other-brand":
        return []
    out = []
    for path, o in iter_role_objects(spec["nodes"], "nodes"):
        role = ctx.roles["roles"].get(o["assetRole"])
        if role and role["generationPolicy"] in RESTRICTED:
            out.append(f"{path}: assetRole '{o['assetRole']}' ({role['generationPolicy']}) is not allowed for brandContext other-brand")
    return out


def rule_registered_asset_ref(ctx, spec):
    out = []
    for path, o in iter_role_objects(spec["nodes"], "nodes"):
        if "assetRef" not in o:
            continue
        role = ctx.roles["roles"].get(o["assetRole"])
        if not role:
            continue  # unknown role: schema enum rejects it
        ref, pol = o["assetRef"], role["generationPolicy"]
        if ref.startswith("generated:"):
            if pol != "may-generate-new":
                out.append(f"{path}: generated asset not allowed for role '{o['assetRole']}' ({pol})")
        elif pol in ("must-reuse-exact", "must-not-fabricate") and ref not in role.get("files", []):
            out.append(f"{path}: assetRef {ref} is not a registered file of role '{o['assetRole']}' ({pol})")
    return out


def rule_max_words(ctx, spec):
    out = []
    for i, n in enumerate(spec["nodes"]):
        d = node_def(ctx, n)
        if d:
            walk_maxwords(d["properties"]["content"], n.get("content", {}), f"nodes[{i}]({n.get('type')}).content", out)
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
    for i, n in enumerate(spec["nodes"]):
        m = n.get("motion")
        if not isinstance(m, dict) or not m.get("reducedMotionFallback"):
            out.append(f"nodes[{i}]({n.get('type')}) motion lacks reducedMotionFallback")
    return out


def check_asset_roles(roles_doc, schema):
    """Registry-level: pinned policies + closure against the schema's assetRole enums."""
    out = []
    roles = roles_doc["roles"]
    for r, pol in PINNED_POLICIES.items():
        if r not in roles:
            out.append(f"pinned role '{r}' missing from asset-roles.json")
        elif roles[r]["generationPolicy"] != pol:
            out.append(f"role '{r}' is pinned to '{pol}' but asset-roles.json says '{roles[r]['generationPolicy']}'")
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
    if used != set(roles):
        out.append(f"schema assetRole enums {sorted(used ^ set(roles))} differ from asset-roles.json")
    return out


def rule_asset_role_pinning(ctx, spec):
    return check_asset_roles(ctx.roles, ctx.schema)


RULE_IMPLS = {
    "TEMPLATE_NODE_SEQUENCE": rule_template_node_sequence,
    "ONE_PER_PAGE": rule_one_per_page,
    "ANNOUNCEMENT_FIRST": rule_announcement_first,
    "HEADER_SECOND": rule_header_second,
    "FOOTER_LAST": rule_footer_last,
    "HEADER_VARIANT_BINDING": rule_header_variant_binding,
    "PRESS_FOLLOWS_HERO": rule_press_follows_hero,
    "ONE_HERO": rule_one_hero,
    "FINAL_CTA_PRECEDES_FOOTER": rule_final_cta_precedes_footer,
    "NO_ADJACENT_CAROUSELS": rule_no_adjacent_carousels,
    "ADJACENT_MARQUEES": rule_adjacent_marquees,
    "MOTION_BUDGET_INFINITE_LOOPS": rule_motion_budget,
    "ROUTE_TEMPLATE_BINDING": rule_route_template_binding,
    "BRAND_CONTEXT_ASSET_POLICY": rule_brand_context_asset_policy,
    "REGISTERED_ASSET_REF": rule_registered_asset_ref,
    "MAX_WORDS": rule_max_words,
    "COMPARISON_MATRIX_SHAPE": rule_comparison_matrix_shape,
    "REDUCED_MOTION_FALLBACK": rule_reduced_motion_fallback,
    "ASSET_ROLE_PINNING": rule_asset_role_pinning,
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


def main(argv):
    paths = argv or [os.path.join(ROOT, "schema/example.pagespec.json")]
    ctx, bad = Ctx(), 0
    for p in paths:
        with open(p) as f:
            spec = json.load(f)
        errors, warns = validate(spec, ctx)
        print(f"{os.path.basename(p)}: {len(errors)} error(s), {len(warns)} warning(s)")
        for e in errors:
            print("  ERROR", e)
        for w in warns:
            print("  WARN ", w)
        bad += bool(errors)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
