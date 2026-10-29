#!/usr/bin/env python3
"""One-shot verification of the Riley-clone design-repo (repositoryVersion 2.0.0).

Usage: python3 extraction/verify_all.py          (needs jsonschema)
Exit 0 = no FAIL. WARN lines are non-fatal (e.g. the sibling source project is absent, as in a standalone/zipped
copy: citation, provenance, leakage-rebuild and source-route cross-checks degrade to warnings).

Checks (each proven to catch drift by extraction/prove_drift.py):
  json            every *.json parses
  allowlist       tokens/llm/component-allowlist.json <-> primitives/components/sections/templates/asset roles/
                  motion patterns/node+page properties/retrieval-ineligible ids (no phantoms, no orphans)
  versions        manifest.allowlistVersion == allowlist.version; manifest.pageSpecVersion == schema const
  counts          registry.manifest.json counts recomputed from the files
  citations       every {"cite": "path:L[-L]", "anchor": ...} resolves inside the real file and contains the anchor
  asset-roles     generationPolicy pins + availability pins (PINNED_AVAILABILITY, re-pinned HERE independently of
                  the validator) + substitutes + schema closure; registered files exist; every public/assets file
                  has a role or a stated reason
  routes          every route the clone serves (routes.jsx exact + pattern routes over src/data/blogPosts.json) and
                  every same-site link in src/ maps to exactly one template; dead slugs + unbuilt links -> not-found
  abs-paths       no machine-absolute path (home directory, private or temp scratch dirs) anywhere in the repo
  entrypoints     manifest entryPoints exist and stay inside design-repo/
  graph           graph.json rule ids == semantic_validate.RULE_IMPLS; severities closed
  examples        every schema/examples/*.pagespec.json validates; one clone AND one generated example per template
                  family; generated examples are mode=generation with zero leakage findings
  scripts         every *.py / *.mjs named in docs/docstrings exists
  responsive      every section has a structured responsive field; required ones are materiallyDifferent + cited
  budgets         section copyBudget == schema x-maxWords
  section-schema  every section contract validates against the closed schema/section-contract.schema.json
  provenance      R7: source {id,tag,file,lines} + semantic {id,category}; semantic.id == id != source.id; the tag
                  opens at the cited start line in the real file; build_provenance.py --check
  retrieval       R8: retrievalEligible pinned (RETRIEVAL_INELIGIBLE_VERIFY here == semantic_validate pin ==
                  contracts == allowlist); runtime-UI-looking ids must be pinned; components too
  wrapper-gate    R9: extraction/wrapper_gate.py (thresholds pinned there and re-asserted here)
  token-catalog   R10: tokens/llm/token-catalog.json == build_token_catalog.py output; policy categories exist
  theme           themes/riley-light.json resolves every semantic color role to its foundation value
  leakage         schema/leakage-patterns.json == build_leakage_patterns.py output (when source present);
                  every pattern family non-empty
  policy          manifest category + designPolicy binding (non-SaaS) + policy file + contentHash recomputed
  motion          every section's motion.pattern lists that section in animation/motion-spec.json
  versions-src    manifest framework versions == ../package.json (WARN if absent)
  readme-counts   README.md <!-- counts --> marker == recomputed counts
  ia              iaSectionIds <-> ../ia.json sections, and ia.json templates <-> templates.json (WARN if absent)
Repo root is derived from __file__.
"""
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.dirname(ROOT)  # sibling source project (may be absent in a standalone copy)
sys.path.insert(0, os.path.join(ROOT, "schema"))
sys.path.insert(0, os.path.join(ROOT, "extraction"))
import semantic_validate as sv  # noqa: E402
import wrapper_gate  # noqa: E402
import policy_hash  # noqa: E402
from jsonschema import Draft7Validator  # noqa: E402

FAILS, WARNS = [], []
DEAD_SLUGS = {"/baby-tracker", "/sleep-tracker", "/sleep-training", "/sleep-regression", "/all-in-one",
              "/your-babys-sleep-simplified", "/product-hunt", "/give-the-gift"}
MUST_BE_RESPONSIVE = {"announcement-bar", "site-header", "faq-clouds", "gradient-band", "blog-teaser", "article-header",
                      "article-toc", "blog-post-grid", "blog-featured-banner"}
TOKEN_LAYERS = ["00-foundation", "10-semantic", "20-component", "30-layout"]
# ---- pins re-asserted here, independently of semantic_validate.py and of the JSON registries
RETRIEVAL_INELIGIBLE_VERIFY = {"cookie-consent"}
RETRIEVAL_INELIGIBLE_COMPONENTS = {"superpower-modal", "mobile-menu"}
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
GATE_PINS = {"VIEWPORT": 1440, "HERO_WARN_PX": 1800, "HERO_ERROR_PX": 3000, "SHARE_WARN": 0.50, "SHARE_ERROR": 0.60, "MIN_INFLOW_SECTIONS": 3}
SAAS_POLICY_ID = "n0-saas-design-constraints-common"


def fail(check, msg):
    FAILS.append(f"[{check}] {msg}")


def warn(check, msg):
    WARNS.append(f"[{check}] {msg}")


def J(rel):
    with open(os.path.join(ROOT, rel)) as f:
        return json.load(f)


def src_present():
    return os.path.isfile(os.path.join(SRC, "package.json")) and os.path.isdir(os.path.join(SRC, "src"))


def all_json():
    return sorted(glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True))


def sections():
    return {json.load(open(p))["id"]: json.load(open(p)) for p in glob.glob(os.path.join(ROOT, "sections", "*.json"))}


# ------------------------------------------------------------------ counts (shared with the manifest + README)
def count_tokens(layer):
    n = 0

    def walk(o):
        nonlocal n
        if isinstance(o, dict):
            if "value" in o or "ref" in o:
                n += 1
                return
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for p in glob.glob(os.path.join(ROOT, "tokens", layer, "*.json")):
        with open(p) as f:
            walk(json.load(f))
    return n


def compute_counts():
    t = J("templates/templates.json")
    g = J("compatibility/graph.json")
    toks = {layer: count_tokens(layer) for layer in TOKEN_LAYERS}
    ex = glob.glob(os.path.join(ROOT, "schema", "examples", "*.pagespec.json"))
    return {
        "tokens": dict(toks, total=sum(toks.values())),
        "catalogTokens": len(J("tokens/llm/token-catalog.json")["tokens"]),
        "primitives": len(glob.glob(os.path.join(ROOT, "primitives", "*.json"))),
        "components": len(glob.glob(os.path.join(ROOT, "components", "*.json"))),
        "sections": len(glob.glob(os.path.join(ROOT, "sections", "*.json"))),
        "templates": len(t["templates"]),
        "templateFamilies": len({v["family"] for v in t["templates"].values()}),
        "routesMapped": len(t["routes"]),
        "articleRoutes": sum(1 for r in t["routes"] if r["template"] == "blog-article"),
        "deadSlugRoutes": sum(1 for r in t["routes"] if r.get("deadSlug")),
        "unbuiltLinkRoutes": sum(1 for r in t["routes"] if r.get("unbuiltLink")),
        "routesExcludedPatterns": len(t["excludedRoutes"]["routes"]),
        "assetRoles": len(J("assets/asset-roles.json")["roles"]),
        "graphRules": len(g["rules"]),
        "motionPatterns": len(J("animation/motion-spec.json")["patterns"]),
        "examples": {"clone": sum(1 for p in ex if ".clone." in p), "generated": sum(1 for p in ex if ".generated." in p)},
    }


# ------------------------------------------------------------------ checks
def check_json():
    for p in all_json():
        try:
            with open(p) as f:
                json.load(f)
        except Exception as e:  # noqa: BLE001
            fail("json", f"{os.path.relpath(p, ROOT)}: {e}")


def schema_node_props(schema):
    props = set()
    for d in schema["definitions"].values():
        props |= set(d["properties"])
    return props


def check_allowlist():
    al = J("tokens/llm/component-allowlist.json")
    schema = J("schema/pagespec.schema.json")
    ids = lambda d: {json.load(open(p))["id"] for p in glob.glob(os.path.join(ROOT, d, "*.json"))}  # noqa: E731
    secs = sections()
    pairs = {
        "primitives": ids("primitives"),
        "components": ids("components"),
        "sections": ids("sections"),
        "templates": set(J("templates/templates.json")["templates"]),
        "assetRoles": set(J("assets/asset-roles.json")["roles"]),
        "motionPatterns": set(J("animation/motion-spec.json")["patterns"]),
        "nodeProperties": schema_node_props(schema),
        "pageProperties": set(schema["properties"]["page"]["properties"]),
        "retrievalIneligible": {k for k, d in secs.items() if d.get("retrievalEligible") is False},
        "overlays": {k for k, d in secs.items() if d.get("placement") == "global-overlay"},
    }
    for k, real in pairs.items():
        listed = set(al.get(k, []))
        if listed - real:
            fail("allowlist", f"{k}: phantom allowlist ids with no contract/schema field: {sorted(listed - real)}")
        if real - listed:
            fail("allowlist", f"{k}: real ids missing from allowlist: {sorted(real - listed)}")
    types = {d["properties"]["type"]["const"] for d in schema["definitions"].values()}
    if types != pairs["sections"]:
        fail("allowlist", f"schema node types != sections/: {sorted(types ^ pairs['sections'])}")
    if set(schema["properties"]["page"]["properties"]["template"]["enum"]) != pairs["templates"]:
        fail("allowlist", "schema template enum != templates.json")
    pats = set()
    for d in schema["definitions"].values():
        pats |= set(d["properties"]["motion"]["properties"]["pattern"]["enum"])
    if not pats <= pairs["motionPatterns"]:
        fail("allowlist", f"schema motion patterns not in motion-spec: {sorted(pats - pairs['motionPatterns'])}")


def check_versions():
    m, al, schema = J("registry.manifest.json"), J("tokens/llm/component-allowlist.json"), J("schema/pagespec.schema.json")
    if m.get("allowlistVersion") != al.get("version"):
        fail("versions", f"manifest.allowlistVersion {m.get('allowlistVersion')} != allowlist.version {al.get('version')}")
    if m.get("pageSpecVersion") != schema["properties"]["pageSpecVersion"]["const"]:
        fail("versions", f"manifest.pageSpecVersion {m.get('pageSpecVersion')} != schema const")
    for p in glob.glob(os.path.join(ROOT, "schema", "examples", "*.pagespec.json")):
        if json.load(open(p)).get("pageSpecVersion") != m.get("pageSpecVersion"):
            fail("versions", f"{os.path.basename(p)} pageSpecVersion != manifest")


def check_counts():
    m = J("registry.manifest.json")
    real = compute_counts()
    for k in set(real) | set(m.get("counts", {})):
        if m.get("counts", {}).get(k) != real.get(k):
            fail("counts", f"manifest counts.{k} = {m.get('counts', {}).get(k)} but files give {real.get(k)}")


CITE_RX = re.compile(r"^(?P<path>[^:]+):(?P<a>\d+)(?:-(?P<b>\d+))?$")
_FILES = {}


def src_lines(path):
    full = os.path.join(SRC, path)
    if full not in _FILES:
        with open(full, encoding="utf-8", errors="replace") as f:
            _FILES[full] = f.read().split("\n")
    return _FILES[full]


def iter_cites(o):
    if isinstance(o, dict):
        if isinstance(o.get("cite"), str):
            yield o
        for v in o.values():
            yield from iter_cites(v)
    elif isinstance(o, list):
        for v in o:
            yield from iter_cites(v)


def check_citations():
    n = absent = 0
    for p in all_json():
        with open(p) as f:
            doc = json.load(f)
        rel = os.path.relpath(p, ROOT)
        for c in iter_cites(doc):
            n += 1
            m = CITE_RX.match(c["cite"])
            if not m:
                fail("citations", f"{rel}: malformed cite {c['cite']}")
                continue
            path, a = m["path"], int(m["a"])
            b = int(m["b"]) if m["b"] else a
            if path.startswith("/") or ".." in path:
                fail("citations", f"{rel}: cite path must be project-relative: {c['cite']}")
                continue
            if not os.path.isfile(os.path.join(SRC, path)):
                absent += 1
                continue
            lines = src_lines(path)
            nlines = len(lines) - (1 if lines and lines[-1] == "" else 0)
            if a < 1 or b < a or b > nlines:
                fail("citations", f"{rel}: {c['cite']} out of range (file has {nlines} lines)")
                continue
            anchor = c.get("anchor")
            if anchor is None:
                fail("citations", f"{rel}: {c['cite']} has no anchor")
            elif anchor not in "\n".join(lines[a - 1:b]):
                fail("citations", f"{rel}: {c['cite']} does not contain anchor {anchor!r}")
    if absent:
        warn("citations", f"{absent}/{n} citations point at source files not present next to this repo (standalone copy?) - range/anchor not checked for those")
    return n


def check_asset_roles():
    roles = J("assets/asset-roles.json")
    for e in sv.check_asset_roles(roles, J("schema/pagespec.schema.json")):
        fail("asset-roles", e)
    if PINNED_AVAILABILITY != sv.PINNED_AVAILABILITY:
        fail("asset-roles", "PINNED_AVAILABILITY in verify_all.py and semantic_validate.py disagree: "
                            f"{sorted(set(PINNED_AVAILABILITY.items()) ^ set(sv.PINNED_AVAILABILITY.items()))}")
    for r, d in roles["roles"].items():
        if d.get("availability") != PINNED_AVAILABILITY.get(r):
            fail("asset-roles", f"role {r}: availability {d.get('availability')!r} != verify_all pin {PINNED_AVAILABILITY.get(r)!r}")
        if d["generationPolicy"] == "must-reuse-exact" and d.get("availability") == "generation-safe":
            fail("asset-roles", f"role {r}: a real Riley mark can never be must-reuse-exact AND generation-safe")
    pub = os.path.join(SRC, "public")
    if not os.path.isdir(pub):
        warn("asset-roles", "public/ not present - registered file existence not checked")
        return
    assigned = set()
    for r, d in roles["roles"].items():
        for fpath in d.get("files", []):
            assigned.add(fpath)
            if not os.path.isfile(os.path.join(pub, fpath.lstrip("/"))):
                fail("asset-roles", f"role {r}: registered file {fpath} missing from public/")
    reasons = roles["unassignedFiles"]["files"]
    for p in glob.glob(os.path.join(pub, "assets", "**", "*"), recursive=True):
        if os.path.isdir(p) or os.path.basename(p) == ".DS_Store":
            continue
        rel = "/" + os.path.relpath(p, pub)
        if rel in assigned or rel in reasons or any(rel.startswith(k) for k in reasons if k.endswith("/")):
            continue
        fail("asset-roles", f"{rel} has no asset role and no stated reason (assets/asset-roles.json unassignedFiles)")


def source_routes():
    """Routes the clone serves: exact routes + pattern routes expanded over the real data (None if source absent)."""
    rpath = os.path.join(SRC, "src", "pages", "routes.jsx")
    if not os.path.isfile(rpath):
        return None
    rjs = open(rpath).read()
    exact = set(re.findall(r"^\s*'(/[^']*)'\s*:", rjs, re.M))
    cats = re.search(r"\^\\/blog\\/\(([a-z|]+)\)\$", rjs)
    cat_routes = {f"/blog/{c}" for c in cats.group(1).split("|")} if cats else set()
    posts = json.load(open(os.path.join(SRC, "src", "data", "blogPosts.json")))
    art = {f"/blog/{p['category']}/{p['slug']}" for p in posts}
    patterns = re.findall(r"^\s*\{\s*test:\s*(/.*?/),", rjs, re.M)
    return exact, cat_routes, art, patterns


def check_routes():
    t = J("templates/templates.json")
    tpls = set(t["templates"])
    seen = {}
    for r in t["routes"]:
        if r["template"] not in tpls:
            fail("routes", f"{r['path']} -> unknown template {r['template']}")
        if r["path"] in seen:
            fail("routes", f"{r['path']} mapped twice")
        seen[r["path"]] = r["template"]
    dead = {r["path"] for r in t["routes"] if r.get("deadSlug")}
    if dead != DEAD_SLUGS:
        fail("routes", f"dead-slug set differs from the 8 measured soft-404 slugs: {sorted(dead ^ DEAD_SLUGS)}")
    for r in t["routes"]:
        if (r.get("deadSlug") or r.get("unbuiltLink")) and r["template"] != "not-found":
            fail("routes", f"{r['path']} is a dead slug / unbuilt link and must map to not-found, got {r['template']}")
    for name in tpls:
        if name not in set(seen.values()):
            fail("routes", f"template {name} has no route")
    if t["excludedRoutes"]["routes"]:
        fail("routes", f"excludedRoutes must be empty (every served route is modelled): {[e['pattern'] for e in t['excludedRoutes']['routes']]}")
    if not src_present():
        warn("routes", "source project absent - routes.jsx / data / href coverage not cross-checked")
        return
    sr = source_routes()
    if sr is None:
        fail("routes", "source present but src/pages/routes.jsx not found")
        return
    exact, cat_routes, art, patterns = sr
    if len(patterns) != 2:
        fail("routes", f"routes.jsx has {len(patterns)} pattern routes; this check expands exactly 2 (category, article) - update it")
    for p in exact | cat_routes:
        if p not in seen:
            fail("routes", f"source route {p} is not mapped")
        elif p in cat_routes and seen[p] != "blog-category":
            fail("routes", f"{p} must map to blog-category")
    mapped_articles = {p for p, tp in seen.items() if tp == "blog-article"}
    if mapped_articles != art:
        fail("routes", f"blog-article routes != src/data/blogPosts.json posts: {sorted(mapped_articles ^ art)[:5]} ...")
    hrefs = set()
    for p in glob.glob(os.path.join(SRC, "src", "**", "*.js"), recursive=True) + glob.glob(os.path.join(SRC, "src", "**", "*.jsx"), recursive=True):
        txt = open(p, encoding="utf-8").read()
        hrefs |= set(re.findall(r"https://(?:www\.)?rileyapp\.com(/[A-Za-z0-9/_-]*)", txt))
        hrefs |= set(re.findall(r"href=\"(/[A-Za-z0-9/_-]*)\"", txt))
        hrefs |= set(re.findall(r"href: '(/[A-Za-z0-9/_-]*)'", txt))
        for m in re.findall(r"href=\{`(/blog/(?:author|reviewer))/\$\{post\.(\w+)\}`\}", txt):
            field = {"authorSlug": "authorSlug", "reviewerSlug": "reviewerSlug"}[m[1]]
            posts = json.load(open(os.path.join(SRC, "src", "data", "blogPosts.json")))
            hrefs |= {f"{m[0]}/{x[field]}" for x in posts if x.get(field)}
    for h in sorted(hrefs):
        h = h.rstrip("/") or "/"
        if h not in seen:
            fail("routes", f"source links to {h} but it is not mapped")


def check_abs_paths():
    needles = ["/" + "Users" + "/", "/" + "private" + "/", "/" + "tmp" + "/", "C:" + "\\" + "Users"]
    for p in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
        if os.path.isdir(p) or "__pycache__" in p:
            continue
        try:
            txt = open(p, encoding="utf-8").read()
        except UnicodeDecodeError:
            continue
        for nd in needles:
            if nd in txt:
                fail("abs-paths", f"{os.path.relpath(p, ROOT)} contains a machine-absolute path ({nd})")


def check_entrypoints():
    for k, rel in J("registry.manifest.json")["entryPoints"].items():
        if rel.startswith("/") or ".." in rel.split("/"):
            fail("entrypoints", f"{k}: {rel} points outside design-repo/")
        elif not os.path.exists(os.path.join(ROOT, rel)):
            fail("entrypoints", f"{k}: {rel} does not exist")


def check_graph():
    g = J("compatibility/graph.json")
    ids = {r["id"] for r in g["rules"]}
    if ids != set(sv.RULE_IMPLS):
        fail("graph", f"graph rule ids != validator RULE_IMPLS: {sorted(ids ^ set(sv.RULE_IMPLS))}")
    for r in g["rules"]:
        if r.get("severity") not in ("error", "warn"):
            fail("graph", f"{r['id']} severity must be error|warn")
    for sid in sections():
        if sid not in g["categories"]:
            fail("graph", f"section {sid} has no graph category")


def check_examples():
    t = J("templates/templates.json")["templates"]
    paths = sorted(glob.glob(os.path.join(ROOT, "schema", "examples", "*.pagespec.json")))
    ctx = sv.Ctx()
    fam_clone, fam_gen = set(), set()
    for p in paths:
        spec = json.load(open(p))
        name = os.path.basename(p)
        errors, warns = sv.validate(spec, ctx)
        for e in errors:
            fail("examples", f"{name}: {e}")
        for w in warns:
            warn("examples", f"{name}: {w}")
        mode = spec["page"]["mode"]
        fam = t[spec["page"]["template"]]["family"]
        if ".generated." in name:
            if mode != "generation":
                fail("examples", f"{name}: a *.generated.* example must be mode=generation")
            fam_gen.add(fam)
        elif ".clone." in name:
            if mode != "clone":
                fail("examples", f"{name}: a *.clone.* example must be mode=clone")
            fam_clone.add(fam)
        else:
            fail("examples", f"{name}: example file name must contain .clone. or .generated.")
    fams = {v["family"] for v in t.values()}
    if fams - fam_clone:
        fail("examples", f"families without a clone example: {sorted(fams - fam_clone)}")
    if fams - fam_gen:
        fail("examples", f"families without a generation-safe example: {sorted(fams - fam_gen)}")


def check_scripts():
    files = [os.path.join(ROOT, "README.md"), os.path.join(ROOT, "CHANGELOG.md"), os.path.join(ROOT, "assets", "README.md")]
    files += glob.glob(os.path.join(ROOT, "**", "*.py"), recursive=True) + glob.glob(os.path.join(ROOT, "**", "*.mjs"), recursive=True)
    for p in files:
        if not os.path.isfile(p):
            fail("scripts", f"{os.path.relpath(p, ROOT)} missing")
            continue
        for ref in set(re.findall(r"([\w./-]+\.(?:py|mjs))\b", open(p).read())):
            ref = ref.lstrip("./")
            if "/" not in ref or ref.startswith("design-repo/"):
                ref = ref.removeprefix("design-repo/")
                if "/" not in ref:
                    continue
            if not os.path.isfile(os.path.join(ROOT, ref)):
                fail("scripts", f"{os.path.relpath(p, ROOT)} references {ref}, which does not exist")


def check_responsive():
    for sid, d in sections().items():
        r = d.get("responsive")
        if not isinstance(r, dict) or not isinstance(r.get("materiallyDifferent"), bool) or not isinstance(r.get("rules"), list):
            fail("responsive", f"{sid}: missing structured responsive field")
            continue
        if sid in MUST_BE_RESPONSIVE and not r["materiallyDifferent"]:
            fail("responsive", f"{sid} has materially different responsive behaviour but is marked otherwise")
        if r["materiallyDifferent"]:
            if not r["rules"]:
                fail("responsive", f"{sid}: materiallyDifferent but no rules")
            for rule in r["rules"]:
                if not rule.get("query") or not rule.get("changes") or not rule.get("evidence"):
                    fail("responsive", f"{sid}: rule needs query, changes and evidence citations")


def budget(sch, path="", out=None):
    out = {} if out is None else out
    if "x-maxWords" in sch:
        out[path] = sch["x-maxWords"]
    if sch.get("type") == "object":
        for k, v in sch["properties"].items():
            budget(v, f"{path}.{k}" if path else k, out)
    if sch.get("type") == "array":
        budget(sch["items"], path + "[]", out)
    return out


def check_budgets():
    schema = J("schema/pagespec.schema.json")
    for sid, d in sections().items():
        ref = d["contentContract"]["schemaRef"]
        cb = d["contentContract"]["copyBudget"]
        if isinstance(ref, dict):
            for v, r in ref.items():
                if cb.get(v) != budget(schema["definitions"][r.split("/")[-1]]["properties"]["content"]):
                    fail("budgets", f"{sid}[{v}] copyBudget != schema x-maxWords")
        elif cb != budget(schema["definitions"][ref.split("/")[-1]]["properties"]["content"]):
            fail("budgets", f"{sid} copyBudget != schema x-maxWords")


def check_section_schema():
    v = Draft7Validator(J("schema/section-contract.schema.json"))
    for sid, d in sections().items():
        for e in v.iter_errors(d):
            fail("section-schema", f"{sid} {list(e.absolute_path)}: {e.message[:140]}")


def check_provenance():
    cats = set(J("schema/section-contract.schema.json")["properties"]["semantic"]["properties"]["category"]["enum"])
    for sid, d in sections().items():
        s, sem = d.get("source"), d.get("semantic")
        if not isinstance(s, dict) or not isinstance(sem, dict):
            fail("provenance", f"{sid}: needs closed source{{}} and semantic{{}} objects")
            continue
        if sem.get("id") != sid:
            fail("provenance", f"{sid}: semantic.id {sem.get('id')!r} must equal the contract id")
        if s.get("id") == sid or s.get("id") == sem.get("id"):
            fail("provenance", f"{sid}: source.id must not equal the semantic id (provenance != taxonomy)")
        if sem.get("category") not in cats:
            fail("provenance", f"{sid}: semantic.category {sem.get('category')!r} not in {sorted(cats)}")
        if not src_present():
            continue
        f = os.path.join(SRC, s.get("file", ""))
        if not os.path.isfile(f):
            fail("provenance", f"{sid}: source.file {s.get('file')} does not exist")
            continue
        a, b = (int(x) for x in s["lines"].split("-"))
        lines = src_lines(s["file"])
        if b > len(lines) or a < 1 or b < a:
            fail("provenance", f"{sid}: source.lines {s['lines']} out of range")
        elif f"<{s['tag']}" not in lines[a - 1]:
            fail("provenance", f"{sid}: <{s['tag']} does not open at {s['file']}:{a}")
    if not src_present():
        warn("provenance", "source project absent - source tag/line ranges not re-read")
        return
    r = subprocess.run([sys.executable, os.path.join(ROOT, "extraction", "build_provenance.py"), "--check"], capture_output=True, text=True)
    if r.returncode:
        fail("provenance", "build_provenance.py --check: " + r.stdout.strip().replace("\n", " | ")[:400])


def check_retrieval():
    secs = sections()
    if RETRIEVAL_INELIGIBLE_VERIFY != sv.RETRIEVAL_INELIGIBLE:
        fail("retrieval", f"RETRIEVAL_INELIGIBLE pins differ: verify_all {sorted(RETRIEVAL_INELIGIBLE_VERIFY)} vs semantic_validate {sorted(sv.RETRIEVAL_INELIGIBLE)}")
    for e in sv.check_retrieval(secs):
        fail("retrieval", e)
    for sid, d in secs.items():
        if (sid in RETRIEVAL_INELIGIBLE_VERIFY) != (d.get("retrievalEligible") is False):
            fail("retrieval", f"{sid}: retrievalEligible {d.get('retrievalEligible')} disagrees with the verify_all pin")
    al = set(J("tokens/llm/component-allowlist.json").get("retrievalIneligible", []))
    if al != RETRIEVAL_INELIGIBLE_VERIFY:
        fail("retrieval", f"allowlist retrievalIneligible {sorted(al)} != pin {sorted(RETRIEVAL_INELIGIBLE_VERIFY)}")
    for p in glob.glob(os.path.join(ROOT, "components", "*.json")):
        c = json.load(open(p))
        pinned = c["id"] in RETRIEVAL_INELIGIBLE_COMPONENTS
        if pinned and (c.get("retrievalEligible") is not False or len(c.get("retrievalReason", "")) < 30):
            fail("retrieval", f"component {c['id']} is runtime UI: needs retrievalEligible:false + 30+ char reason")
        if not pinned and c.get("retrievalEligible") is False:
            fail("retrieval", f"component {c['id']} is retrievalEligible:false but not pinned")
        if sv.RUNTIME_UI_RX.search(c["id"]) and not pinned:
            fail("retrieval", f"component {c['id']} looks like runtime UI but is not pinned")


def check_wrapper_gate():
    for k, v in GATE_PINS.items():
        if getattr(wrapper_gate, k) != v:
            fail("wrapper-gate", f"wrapper_gate.{k} = {getattr(wrapper_gate, k)} but the pinned value is {v}")
    errors, warns = wrapper_gate.run()
    for e in errors:
        fail("wrapper-gate", e)
    for w in warns:
        warn("wrapper-gate", w)


def check_token_catalog():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "extraction", "build_token_catalog.py"), "--check"], capture_output=True, text=True)
    if r.returncode:
        fail("token-catalog", r.stdout.strip())
    cat, pol = J("tokens/llm/token-catalog.json"), J("tokens/llm/token-policy.json")
    for key in pol["rawValueRestrictions"]:
        if key not in cat["categories"]:
            fail("token-catalog", f"policy category '{key}' not a token-catalog category")
    for prop, cs in pol["propertyCategories"].items():
        if set(cs) != sv.STYLE_PROPERTY_CATEGORIES.get(prop):
            fail("token-catalog", f"token-policy propertyCategories.{prop} {cs} != validator {sorted(sv.STYLE_PROPERTY_CATEGORIES.get(prop, []))}")
        for c in cs:
            if c not in cat["categories"]:
                fail("token-catalog", f"policy property {prop} -> unknown catalog category {c}")
    rules = {r["id"] for r in J("compatibility/graph.json")["rules"] if r["id"].startswith("TOKEN_")}
    if set(pol["rules"]) != rules:
        fail("token-catalog", f"token-policy rules {sorted(pol['rules'])} != graph TOKEN_* rules {sorted(rules)}")


def check_theme():
    fnd = J("tokens/00-foundation/color.json")["tokens"]
    roles = J("tokens/10-semantic/color-roles.json")["roles"]
    theme = J("tokens/themes/riley-light.json")["colorRoles"]
    if set(theme) != set(roles):
        fail("theme", f"theme roles != semantic roles: {sorted(set(theme) ^ set(roles))}")
    for k, v in roles.items():
        base = fnd.get(v["ref"].split(".")[-1], {}).get("value")
        got = theme.get(k)
        got = got["base"] if isinstance(got, dict) else got
        if base is None or got != base:
            fail("theme", f"{k}: theme {got} != foundation {base}")


def check_leakage():
    P = J("schema/leakage-patterns.json")
    for fam in ("brand", "persons", "organizations", "claims", "domains", "embedIds", "storeMarks", "ratings"):
        if not P.get(fam):
            fail("leakage", f"leakage pattern family '{fam}' is empty")
        for e in P.get(fam, []):
            if not e.get("evidence"):
                fail("leakage", f"{fam} entry {e} has no file:line evidence")
    if P["copyShingles"]["count"] != len(P["copyShingles"]["hashes"]) or P["copyShingles"]["count"] < 1000:
        fail("leakage", "copyShingles count/hashes inconsistent or implausibly small")
    if P.get("humanReviewed") is not False:
        fail("leakage", "leakage-patterns.json must state humanReviewed:false (no human reviewed the pinned patterns)")
    if not src_present():
        warn("leakage", "source project absent - leakage registry not rebuilt from source")
        return
    r = subprocess.run([sys.executable, os.path.join(ROOT, "extraction", "build_leakage_patterns.py"), "--check"], capture_output=True, text=True)
    if r.returncode:
        fail("leakage", r.stdout.strip())


def check_policy():
    m = J("registry.manifest.json")
    dp = m.get("designPolicy") or {}
    if m.get("category") != "consumer-app":
        fail("policy", f"manifest category {m.get('category')!r} must be 'consumer-app' (non-SaaS, see policy classificationEvidence)")
    for k in ("ref", "policyId", "policyVersion", "commonIrVersion", "enforcementMode", "contentHash"):
        if not dp.get(k):
            fail("policy", f"manifest designPolicy.{k} missing")
    if dp.get("policyId") == SAAS_POLICY_ID:
        fail("policy", "a consumer app must not bind the SaaS common policy")
    if dp.get("commonIrVersion") != "0.5" or dp.get("enforcementMode") != "hard-and-soft":
        fail("policy", "designPolicy must declare commonIrVersion 0.5 and enforcementMode hard-and-soft")
    ref = dp.get("ref", "")
    if not os.path.isfile(os.path.join(ROOT, ref)):
        fail("policy", f"policy file {ref} missing")
        return
    pol = J(ref)
    if pol.get("policyId") != dp.get("policyId") or pol.get("policyVersion") != dp.get("policyVersion") or pol.get("commonIrVersion") != dp.get("commonIrVersion"):
        fail("policy", "manifest designPolicy id/version/commonIrVersion != policy file")
    cl = pol.get("classification", {})
    if cl.get("isSaaS") is not False:
        fail("policy", "policy classification.isSaaS must be false")
    for k in ("productCategory", "productDomain", "surfaces", "audiences"):
        if not cl.get(k):
            fail("policy", f"policy classification.{k} missing")
    if SAAS_POLICY_ID not in pol.get("notBoundTo", {}) or len(pol["notBoundTo"].get(SAAS_POLICY_ID, "")) < 30:
        fail("policy", f"policy must state notBoundTo.{SAAS_POLICY_ID} with a reason")
    if SAAS_POLICY_ID not in (dp.get("notBoundTo") or []):
        fail("policy", f"manifest designPolicy.notBoundTo must list {SAAS_POLICY_ID}")
    ap = pol.get("approval", {})
    if ap.get("policyDecision") != "defined-pending-architecture-review" or ap.get("architectureDecisionRecorded") is not False:
        fail("policy", "policy approval must be defined-pending-architecture-review with architectureDecisionRecorded false")
    for rel in pol.get("enforcedBy", []):
        if not os.path.isfile(os.path.join(ROOT, rel)):
            fail("policy", f"enforcedBy file {rel} missing")
    if not pol.get("generationRules"):
        fail("policy", "policy generationRules missing")
    real = policy_hash.compute(ROOT)
    if dp.get("contentHash") != real:
        fail("policy", f"designPolicy.contentHash {dp.get('contentHash')} != recomputed {real} (run extraction/policy_hash.py --write after review)")


def check_motion():
    pats = J("animation/motion-spec.json")["patterns"]
    for sid, d in sections().items():
        p = d["motion"]["pattern"]
        if p not in pats:
            fail("motion", f"{sid}: unknown motion pattern {p}")
        elif sid not in pats[p]["sections"]:
            fail("motion", f"{sid}: motion-spec pattern {p} does not list it")
        elif d["motion"]["reducedMotionFallback"] != pats[p]["reducedMotionFallback"]:
            fail("motion", f"{sid}: reducedMotionFallback differs from motion-spec {p}")


def check_versions_src():
    if not src_present():
        warn("versions-src", "../package.json absent - framework versions not re-diffed")
        return
    pkg = json.load(open(os.path.join(SRC, "package.json")))
    deps = dict(pkg.get("dependencies", {}), **pkg.get("devDependencies", {}))
    for name, ver in J("registry.manifest.json")["sourceProject"]["frameworkVersions"].items():
        if deps.get(name) != ver:
            fail("versions-src", f"manifest says {name} {ver}, package.json says {deps.get(name)}")


def check_ia():
    p = os.path.join(SRC, "ia.json")
    if not os.path.isfile(p):
        warn("ia", "../ia.json absent - IA crosswalk not checked")
        return
    doc = json.load(open(p))
    ia = set(doc["sections"])
    mine = {}
    for sid, d in sections().items():
        for x in d.get("iaSectionIds", []):
            mine[x] = sid
    if set(mine) - ia:
        fail("ia", f"iaSectionIds not in ia.json: {sorted(set(mine) - ia)}")
    if ia - set(mine):
        fail("ia", f"ia.json sections without a section contract: {sorted(ia - set(mine))}")
    tpl = J("templates/templates.json")["templates"]
    by_ia = {v["iaTemplateId"]: k for k, v in tpl.items()}
    for t in doc["templates"]:
        k = by_ia.get(t["id"])
        if not k:
            fail("ia", f"ia.json template {t['id']} has no design-repo template")
            continue
        want = {s for n in tpl[k]["nodes"] for s in [n["section"]]}
        got = {mine.get(s) for s in t["sections"]} - {"cookie-consent"}
        if want != got:
            fail("ia", f"{t['id']}: ia sections map to {sorted(x for x in got if x)} but template {k} has {sorted(want)}")
    if len(doc["templates"]) != len(tpl):
        fail("ia", f"ia.json has {len(doc['templates'])} templates, design-repo {len(tpl)}")
    if doc["meta"].get("totalRoutes") != sum(1 for r in J("templates/templates.json")["routes"] if r["path"] != "*"):
        fail("ia", f"ia.json meta.totalRoutes {doc['meta'].get('totalRoutes')} != mapped concrete routes")


def check_readme_counts():
    txt = open(os.path.join(ROOT, "README.md")).read() if os.path.isfile(os.path.join(ROOT, "README.md")) else ""
    m = re.search(r"<!-- counts:(\{.*?\}) -->", txt)
    if not m:
        fail("readme-counts", "README.md lacks the <!-- counts:{...} --> marker")
    elif json.loads(m.group(1)) != compute_counts():
        fail("readme-counts", "README.md counts marker differs from counts recomputed from files")


CHECKS = [check_readme_counts, check_json, check_allowlist, check_versions, check_counts, check_citations, check_asset_roles,
          check_routes, check_abs_paths, check_entrypoints, check_graph, check_examples, check_scripts, check_responsive,
          check_budgets, check_section_schema, check_provenance, check_retrieval, check_wrapper_gate, check_token_catalog,
          check_theme, check_leakage, check_policy, check_motion, check_versions_src, check_ia]


def main():
    print(f"design-repo root: {os.path.basename(ROOT)}  (source project present: {src_present()})")
    ncites = None
    for c in CHECKS:
        before = len(FAILS)
        r = c()
        if c is check_citations:
            ncites = r
        print(f"  {'ok  ' if len(FAILS) == before else 'FAIL'} {c.__name__.replace('check_', '')}")
    print(f"citations scanned: {ncites}; counts: {json.dumps(compute_counts())}")
    for w in WARNS:
        print("WARN", w)
    for f in FAILS:
        print("FAIL", f)
    print(f"\nRESULT: {'PASS' if not FAILS else 'FAIL'} ({len(FAILS)} fail, {len(WARNS)} warn)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
