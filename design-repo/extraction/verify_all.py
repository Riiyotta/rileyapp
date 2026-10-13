#!/usr/bin/env python3
"""One-shot verification of the Riley-clone design-repo.

Usage: python3 extraction/verify_all.py
Exit 0 = no FAIL. WARN lines are non-fatal (e.g. the sibling source project is absent,
as in a standalone/zipped copy: citation and source cross-checks degrade to warnings).

Checks (each proven to catch drift by scratch-copy injection, see CHANGELOG.md):
  json            every *.json parses
  allowlist       tokens/llm/component-allowlist.json <-> primitives/components/sections/
                  templates/asset roles/motion patterns/node+page properties (no phantoms, no orphans)
  versions        manifest.allowlistVersion == allowlist.version; manifest.pageSpecVersion == schema const
  counts          registry.manifest.json counts recomputed from the files
  citations       every {"cite": "path:L[-L]", "anchor": ...} resolves inside the real file AND
                  the anchor text occurs in that line range (WARN if the source file is absent)
  asset-roles     pinned generationPolicy values (semantic_validate.PINNED_POLICIES) + closure with the
                  schema; registered files exist; every public/assets file has a role or a stated reason
  routes          every route maps to exactly one existing template; 8 dead slugs -> not-found;
                  exclusions don't overlap mappings; source routes.js(x) + every rileyapp.com/... or "/x"
                  href in src/ is mapped or excluded
  abs-paths       no machine-absolute home-directory path anywhere in the repo
  entrypoints     manifest entryPoints exist and stay inside design-repo/
  graph           graph.json rule ids == semantic_validate.RULE_IMPLS
  example         example.pagespec.json passes schema + semantic validation
  scripts         every *.py named in README/CHANGELOG/docstrings exists
  responsive      every section has a structured responsive field; required ones are materiallyDifferent with citations
  budgets         section copyBudget == schema x-maxWords
  token-policy    policy category keys exist in token-catalog; catalog files exist
  theme           themes/riley-light.json resolves every semantic color role to its foundation value
  versions-src    manifest framework versions == ../package.json (WARN if absent)
  readme-counts   README.md <!-- counts --> marker == recomputed counts
  ia              iaSectionIds <-> ../ia.json sections (WARN if absent)
Repo root is derived from __file__.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.dirname(ROOT)  # sibling source project (may be absent in a standalone copy)
sys.path.insert(0, os.path.join(ROOT, "schema"))
import semantic_validate as sv  # noqa: E402

FAILS, WARNS = [], []
DEAD_SLUGS = {"/baby-tracker", "/sleep-tracker", "/sleep-training", "/sleep-regression", "/all-in-one",
              "/your-babys-sleep-simplified", "/product-hunt", "/give-the-gift"}
MUST_BE_RESPONSIVE = {"announcement-bar", "site-header", "faq-clouds", "gradient-band", "blog-teaser"}
TOKEN_LAYERS = ["00-foundation", "10-semantic", "20-component", "30-layout"]


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


# ------------------------------------------------------------------ counts (shared with the manifest)
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
    return {
        "tokens": dict(toks, total=sum(toks.values())),
        "primitives": len(glob.glob(os.path.join(ROOT, "primitives", "*.json"))),
        "components": len(glob.glob(os.path.join(ROOT, "components", "*.json"))),
        "sections": len(glob.glob(os.path.join(ROOT, "sections", "*.json"))),
        "templates": len(t["templates"]),
        "routesMapped": len(t["routes"]),
        "deadSlugRoutes": sum(1 for r in t["routes"] if r.get("deadSlug")),
        "routesExcludedPatterns": len(t["excludedRoutes"]["routes"]),
        "assetRoles": len(J("assets/asset-roles.json")["roles"]),
        "graphRules": len(g["rules"]),
        "motionPatterns": len(J("animation/motion-spec.json")["patterns"]),
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
    pairs = {
        "primitives": ids("primitives"),
        "components": ids("components"),
        "sections": ids("sections"),
        "templates": set(J("templates/templates.json")["templates"]),
        "assetRoles": set(J("assets/asset-roles.json")["roles"]),
        "motionPatterns": set(J("animation/motion-spec.json")["patterns"]),
        "nodeProperties": schema_node_props(schema),
        "pageProperties": set(schema["properties"]["page"]["properties"]),
    }
    for k, real in pairs.items():
        listed = set(al.get(k, []))
        if listed - real:
            fail("allowlist", f"{k}: phantom allowlist ids with no contract/schema field: {sorted(listed - real)}")
        if real - listed:
            fail("allowlist", f"{k}: real ids missing from allowlist: {sorted(real - listed)}")
    # schema enums must agree with the same registries
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


def check_counts():
    m = J("registry.manifest.json")
    real = compute_counts()
    if m.get("counts") != real:
        for k in real:
            if m.get("counts", {}).get(k) != real[k]:
                fail("counts", f"manifest counts.{k} = {m.get('counts', {}).get(k)} but files give {real[k]}")


CITE_RX = re.compile(r"^(?P<path>[^:]+):(?P<a>\d+)(?:-(?P<b>\d+))?$")


def iter_cites(o):
    if isinstance(o, dict):
        if "cite" in o:
            yield o
        for v in o.values():
            yield from iter_cites(v)
    elif isinstance(o, list):
        for v in o:
            yield from iter_cites(v)


def check_citations():
    n = absent = 0
    cache = {}
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
            full = os.path.join(SRC, path)
            if path.startswith("/") or ".." in path:
                fail("citations", f"{rel}: cite path must be project-relative: {c['cite']}")
                continue
            if not os.path.isfile(full):
                absent += 1
                continue
            if full not in cache:
                with open(full, encoding="utf-8", errors="replace") as f:
                    cache[full] = f.read().split("\n")
            lines = cache[full]
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
    for p in DEAD_SLUGS:
        if seen.get(p) != "not-found":
            fail("routes", f"dead slug {p} must map to not-found, got {seen.get(p)}")
    pats = [e["pattern"] for e in t["excludedRoutes"]["routes"]]
    for e in t["excludedRoutes"]["routes"]:
        if not e.get("reason") or e.get("status") not in ("pending", "unverified"):
            fail("routes", f"excluded {e['pattern']} needs a reason and status pending|unverified")
    for p in seen:
        if p != "*" and sv.excluded_match(p, pats):
            fail("routes", f"{p} is both mapped and excluded")
    for name in tpls:
        if name not in set(seen.values()):
            fail("routes", f"template {name} has no route")
    if not src_present():
        warn("routes", "source project absent - routes.js / href coverage not cross-checked")
        return
    rpath = next((os.path.join(SRC, "src/pages", f) for f in ("routes.jsx", "routes.js") if os.path.isfile(os.path.join(SRC, "src/pages", f))), None)
    if not rpath:
        fail("routes", "source present but src/pages/routes.js(x) not found")
        return
    rjs = open(rpath).read()
    exact = re.findall(r"^\s*'(/[^']*)'\s*:", rjs, re.M)
    for p in exact:
        if p in seen:
            continue
        if sv.excluded_match(p, pats):
            warn("routes", f"source route {p} is BUILT in {os.path.basename(rpath)} but excluded/pending in this snapshot (source advanced beyond snapshot)")
        else:
            fail("routes", f"source route {p} is neither mapped nor excluded")
    active = re.findall(r"^\s*\{\s*test:\s*(/.*?/),", rjs, re.M)
    for a in active:
        warn("routes", f"source pattern route {a} is ACTIVE in {os.path.basename(rpath)}; excluded/pending in this snapshot")
    hrefs = set()
    for p in glob.glob(os.path.join(SRC, "src", "**", "*.js*"), recursive=True):
        txt = open(p, encoding="utf-8").read()
        hrefs |= set(re.findall(r"https://(?:www\.)?rileyapp\.com(/[A-Za-z0-9/_-]*)", txt))
        hrefs |= set(re.findall(r"href=\"(/[A-Za-z0-9/_-]*)\"", txt))
    for h in sorted(hrefs):
        h = h.rstrip("/") or "/"
        if h in seen or sv.excluded_match(h, pats):
            continue
        fail("routes", f"source links to {h} but it is neither mapped nor excluded")


def check_abs_paths():
    needle = "/" + "Users" + "/"
    for p in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
        if os.path.isdir(p) or "__pycache__" in p:
            continue
        try:
            txt = open(p, encoding="utf-8").read()
        except UnicodeDecodeError:
            continue
        if needle in txt:
            fail("abs-paths", f"{os.path.relpath(p, ROOT)} contains an absolute home-directory path")


def check_entrypoints():
    for k, rel in J("registry.manifest.json")["entryPoints"].items():
        if rel.startswith("/") or ".." in rel.split("/"):
            fail("entrypoints", f"{k}: {rel} points outside design-repo/")
        elif not os.path.exists(os.path.join(ROOT, rel)):
            fail("entrypoints", f"{k}: {rel} does not exist")


def check_graph():
    ids = {r["id"] for r in J("compatibility/graph.json")["rules"]}
    if ids != set(sv.RULE_IMPLS):
        fail("graph", f"graph rule ids != validator RULE_IMPLS: {sorted(ids ^ set(sv.RULE_IMPLS))}")
    for r in J("compatibility/graph.json")["rules"]:
        if r.get("severity") not in ("error", "warn"):
            fail("graph", f"{r['id']} severity must be error|warn")


def check_example():
    errors, warns = sv.validate(J("schema/example.pagespec.json"))
    for e in errors:
        fail("example", e)
    for w in warns:
        warn("example", w)


def check_scripts():
    files = [os.path.join(ROOT, "README.md"), os.path.join(ROOT, "CHANGELOG.md"), os.path.join(ROOT, "assets", "README.md")]
    files += glob.glob(os.path.join(ROOT, "**", "*.py"), recursive=True)
    for p in files:
        if not os.path.isfile(p):
            fail("scripts", f"{os.path.relpath(p, ROOT)} missing")
            continue
        for ref in set(re.findall(r"([\w./-]+\.py)\b", open(p).read())):
            ref = ref.lstrip("./")
            if "/" not in ref:
                continue
            if not os.path.isfile(os.path.join(ROOT, ref)):
                fail("scripts", f"{os.path.relpath(p, ROOT)} references {ref}, which does not exist")


def check_responsive():
    for p in glob.glob(os.path.join(ROOT, "sections", "*.json")):
        d = json.load(open(p))
        r = d.get("responsive")
        if not isinstance(r, dict) or not isinstance(r.get("materiallyDifferent"), bool) or not isinstance(r.get("rules"), list):
            fail("responsive", f"{d['id']}: missing structured responsive field")
            continue
        if d["id"] in MUST_BE_RESPONSIVE and not r["materiallyDifferent"]:
            fail("responsive", f"{d['id']} has materially different responsive behaviour but is marked otherwise")
        if r["materiallyDifferent"]:
            if not r["rules"]:
                fail("responsive", f"{d['id']}: materiallyDifferent but no rules")
            for rule in r["rules"]:
                if not rule.get("query") or not rule.get("changes") or not rule.get("evidence"):
                    fail("responsive", f"{d['id']}: rule needs query, changes and evidence citations")


def check_budgets():
    schema = J("schema/pagespec.schema.json")

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
    for p in glob.glob(os.path.join(ROOT, "sections", "*.json")):
        d = json.load(open(p))
        ref = d["contentContract"]["schemaRef"]
        cb = d["contentContract"]["copyBudget"]
        if isinstance(ref, dict):
            for v, r in ref.items():
                real = budget(schema["definitions"][r.split("/")[-1]]["properties"]["content"])
                if cb.get(v) != real:
                    fail("budgets", f"{d['id']}[{v}] copyBudget != schema x-maxWords")
        else:
            real = budget(schema["definitions"][ref.split("/")[-1]]["properties"]["content"])
            if cb != real:
                fail("budgets", f"{d['id']} copyBudget != schema x-maxWords")


def check_token_policy():
    cat, pol = J("tokens/llm/token-catalog.json"), J("tokens/llm/token-policy.json")
    for key in pol["rawValueRestrictions"]:
        if key not in cat["categories"]:
            fail("token-policy", f"policy category '{key}' not a token-catalog category")
    for k, ref in cat["categories"].items():
        rel = ref.replace("tokens.", "tokens/", 1).replace(".", "/", 1) + ".json"
        if not os.path.isfile(os.path.join(ROOT, rel)):
            fail("token-policy", f"catalog category {k} -> {rel} missing")


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
    secs = doc["sections"]
    ia = set(secs) if isinstance(secs, dict) else {x["id"] for x in secs}
    tpls = doc["templates"]
    tpls = tpls.values() if isinstance(tpls, dict) else tpls
    in_scope = set()
    for t in tpls:
        if t.get("id") in ("template.home", "template.pricing", "template.not-found"):
            in_scope |= set(t.get("sections", []))
    mine = set()
    for f in glob.glob(os.path.join(ROOT, "sections", "*.json")):
        mine |= set(json.load(open(f)).get("iaSectionIds", []))
    overlays = {o.get("iaSectionId") for o in J("templates/templates.json").get("unmodelledGlobalOverlays", [])}
    if mine - ia:
        fail("ia", f"iaSectionIds not in ia.json: {sorted(mine - ia)}")
    if in_scope - mine - overlays:
        fail("ia", f"IA sections on home/pricing/not-found not covered by a section contract or a declared overlay: {sorted(in_scope - mine - overlays)}")
    out = ia - in_scope
    if out:
        warn("ia", f"{len(out)} IA sections belong to templates outside this snapshot (blog/text/legal) - not modelled")


def check_readme_counts():
    txt = open(os.path.join(ROOT, "README.md")).read() if os.path.isfile(os.path.join(ROOT, "README.md")) else ""
    m = re.search(r"<!-- counts:(\{.*?\}) -->", txt)
    if not m:
        fail("readme-counts", "README.md lacks the <!-- counts:{...} --> marker")
    elif json.loads(m.group(1)) != compute_counts():
        fail("readme-counts", "README.md counts marker differs from counts recomputed from files")


CHECKS = [check_readme_counts, check_json, check_allowlist, check_versions, check_counts, check_citations, check_asset_roles, check_routes,
          check_abs_paths, check_entrypoints, check_graph, check_example, check_scripts, check_responsive, check_budgets,
          check_token_policy, check_theme, check_versions_src, check_ia]


def main():
    print(f"design-repo root: {os.path.basename(ROOT)}  (source project present: {src_present()})")
    ncites = None
    for c in CHECKS:
        before = len(FAILS)
        r = c()
        if c is check_citations:
            ncites = r
        name = c.__name__.replace("check_", "")
        print(f"  {'ok  ' if len(FAILS) == before else 'FAIL'} {name}")
    print(f"citations scanned: {ncites}; counts: {json.dumps(compute_counts())}")
    for w in WARNS:
        print("WARN", w)
    for f in FAILS:
        print("FAIL", f)
    print(f"\nRESULT: {'PASS' if not FAILS else 'FAIL'} ({len(FAILS)} fail, {len(WARNS)} warn)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
