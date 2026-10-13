#!/usr/bin/env python3
"""Adversarial suite for the Riley-clone PageSpec contract.

Usage: python3 schema/tests/adversarial_test.py

CONTROLS (must produce zero errors):
  * schema/example.pagespec.json
  * one PageSpec auto-synthesized per template in templates/templates.json (built
    generically from the schema + template node list, so a new template is covered
    with no new code)
  * a dead sitemap slug bound to the not-found template
MUTATIONS (each must be rejected with >=1 error): see CASES below.
Exit 0 only if every control passes and every mutation is rejected.
Root derived from __file__ (no absolute paths).
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "schema"))
import semantic_validate as sv  # noqa: E402

CTX = sv.Ctx()
EXAMPLE = json.load(open(os.path.join(ROOT, "schema/example.pagespec.json")))


# ------------------------------------------------------------------ generic synthesizer
def synth(sch):
    if "$ref" in sch:
        return synth(CTX.schema["definitions"][sch["$ref"].split("/")[-1]])
    if "const" in sch:
        return copy.deepcopy(sch["const"])
    if "enum" in sch:
        return sch["enum"][0]
    t = sch.get("type")
    if t == "object":
        props = sch["properties"]
        out = {}
        for k in sch.get("required", []):
            out[k] = synth(props[k])
        if "assetRole" in out and "assetRef" in out:
            role = CTX.roles["roles"][out["assetRole"]]
            out["assetRef"] = role["files"][0] if role.get("files") else "generated:placeholder"
        return out
    if t == "array":
        return [synth(sch["items"]) for _ in range(sch.get("minItems", 0))]
    if t == "boolean":
        return False
    if t == "string":
        return "Placeholder"
    raise ValueError(f"cannot synthesize {sch}")


def synth_page(tname):
    tpl = CTX.templates["templates"][tname]
    route = next(r["path"] for r in CTX.templates["routes"] if r["template"] == tname)
    nodes = []
    for tn in tpl["nodes"]:
        sid, var = tn["section"], tn.get("variant")
        dn = f"node_{sid}__{var}" if var and f"node_{sid}__{var}" in CTX.schema["definitions"] else f"node_{sid}"
        n = synth(CTX.schema["definitions"][dn])
        if var:
            n["variant"] = var
        nodes.append(n)
    return {"pageSpecVersion": "1.0.0", "page": {"route": route, "title": "Placeholder", "template": tname,
                                                 "brandContext": "riley-clone", "theme": "riley-light"}, "nodes": nodes}


# ------------------------------------------------------------------ helpers
def ex():
    return copy.deepcopy(EXAMPLE)


def find(spec, t):
    return next(n for n in spec["nodes"] if n["type"] == t)


def idx(spec, t):
    return next(i for i, n in enumerate(spec["nodes"]) if n["type"] == t)


def m_wrong_enum():
    s = ex(); s["page"]["theme"] = "riley-dark"; return s

def m_missing_required():
    s = ex(); del find(s, "hero-home")["content"]["heading"]; return s

def m_invented_type():
    s = ex(); s["nodes"].insert(3, {"type": "hero-video", "content": {}, "motion": {"pattern": "static", "reducedMotionFallback": "x"}}); return s

def m_missing_rmf():
    s = ex(); del find(s, "faq-clouds")["motion"]["reducedMotionFallback"]; return s

def m_invented_motion_field():
    s = ex(); find(s, "clinical-board")["motion"]["scrollReveal"] = "fade-up"; return s

def m_wrong_motion_pattern():
    s = ex(); find(s, "press-marquee")["motion"]["pattern"] = "embla-loop"; return s

def m_scroll_reveal_pattern():
    s = ex(); find(s, "how-riley-works")["motion"]["pattern"] = "fade-up-on-scroll"; return s

def m_duplicate_one_per_page():
    s = ex(); i = idx(s, "faq-clouds"); s["nodes"].insert(i + 1, copy.deepcopy(s["nodes"][i])); return s

def m_removed_required():
    s = ex(); s["nodes"].pop(idx(s, "clinical-board")); return s

def m_reordered_footer():
    s = ex(); f = s["nodes"].pop(idx(s, "site-footer")); s["nodes"].insert(idx(s, "final-cta"), f); return s

def m_reordered_announcement():
    s = ex(); a = s["nodes"].pop(0); s["nodes"].insert(2, a); return s

def m_template_mismatch():
    s = ex(); s["page"]["template"] = "pricing"; s["page"]["route"] = "/pricing"; return s

def m_gradient_variant_on_home():
    s = ex(); g = find(s, "gradient-band"); g["variant"] = "table-only"; del g["content"]["featureCards"]; return s

def m_header_variant_on_home():
    s = ex(); find(s, "site-header")["variant"] = "standalone"; return s

def m_max_words():
    s = ex(); find(s, "hero-home")["content"]["heading"] = " ".join(["Panic"] * 30); return s

def m_max_words_nested():
    s = ex(); find(s, "faq-clouds")["content"]["items"][0]["answer"] = " ".join(["word"] * 81); return s

def m_invented_asset_role():
    s = ex(); find(s, "clinical-board")["content"]["advisors"][0]["portrait"]["assetRole"] = "stock-photo"; return s

def m_wrong_role_for_field():
    s = ex(); p = find(s, "clinical-board")["content"]["advisors"][0]["portrait"]; p["assetRole"] = "press-logo"; p["assetRef"] = "/assets/nbc.png"; return s

def m_fabricated_portrait():
    s = ex(); find(s, "clinical-board")["content"]["advisors"][0]["portrait"]["assetRef"] = "/assets/generated-doctor.png"; return s

def m_generated_press_logo():
    s = ex(); find(s, "press-marquee")["content"]["logos"][0]["assetRef"] = "generated:new-press-logo"; return s

def m_live_endpoint_href():
    s = ex(); find(s, "final-cta")["content"]["cta"]["href"] = "https://rileyapp.onelink.me/JNxh/nativeappstorebutton"; return s

def m_other_brand_reuses_mascot():
    s = ex(); s["page"]["brandContext"] = "other-brand"; return s

def m_dead_slug_landing():
    s = ex(); s["page"]["route"] = "/baby-tracker"; return s

def m_excluded_route():
    s = ex(); s["page"]["route"] = "/blog/sleep/baby-witching-hour"; return s

def m_matrix_shape():
    s = ex(); find(s, "gradient-band")["content"]["comparisonTable"]["rows"][0]["marks"].pop(); return s


CASES = [
    ("wrong enum (theme riley-dark)", m_wrong_enum),
    ("missing required field (hero-home.content.heading)", m_missing_required),
    ("invented section type 'hero-video'", m_invented_type),
    ("missing reducedMotionFallback (faq-clouds)", m_missing_rmf),
    ("invented motion field 'scrollReveal'", m_invented_motion_field),
    ("wrong per-section motion pattern (press-marquee -> embla-loop)", m_wrong_motion_pattern),
    ("invented scroll-reveal motion pattern", m_scroll_reveal_pattern),
    ("duplicate one-per-page section (faq-clouds x2)", m_duplicate_one_per_page),
    ("removed required section (clinical-board)", m_removed_required),
    ("reordered fixed-position section (footer before final-cta)", m_reordered_footer),
    ("reordered fixed-position section (announcement-bar not first)", m_reordered_announcement),
    ("template/node mismatch (home nodes declared as pricing)", m_template_mismatch),
    ("(section, variant): gradient-band table-only on home", m_gradient_variant_on_home),
    ("(section, variant): site-header standalone before hero-home", m_header_variant_on_home),
    ("maxWords overflow (hero heading 30 words)", m_max_words),
    ("maxWords overflow nested (faq answer 81 words)", m_max_words_nested),
    ("invented assetRole 'stock-photo'", m_invented_asset_role),
    ("assetRole not allowed for field (press-logo as advisor portrait)", m_wrong_role_for_field),
    ("fabricated file for must-not-fabricate role (advisor portrait)", m_fabricated_portrait),
    ("generated: ref for must-not-fabricate role (press logo)", m_generated_press_logo),
    ("live onelink smuggled as href", m_live_endpoint_href),
    ("other-brand page reusing Riley mascots/logos/photos", m_other_brand_reuses_mascot),
    ("dead sitemap slug /baby-tracker bound to landing template 'home'", m_dead_slug_landing),
    ("excluded/pending route /blog/{category}/{slug}", m_excluded_route),
    ("comparison matrix row/column mismatch", m_matrix_shape),
]


def registry_cases():
    """Mutations of registries rather than PageSpecs."""
    res = []
    # re-pin a real-weighted role to a DIFFERENT BUT VALID policy
    roles = copy.deepcopy(CTX.roles)
    roles["roles"]["press-logo"]["generationPolicy"] = "may-generate-new"
    res.append(("re-pinned asset role press-logo -> may-generate-new (valid enum value)", sv.check_asset_roles(roles, CTX.schema)))
    roles = copy.deepcopy(CTX.roles)
    roles["roles"]["app-store-onelink"]["generationPolicy"] = "must-reuse-exact"
    res.append(("re-pinned endpoint app-store-onelink -> must-reuse-exact (valid enum value)", sv.check_asset_roles(roles, CTX.schema)))
    roles = copy.deepcopy(CTX.roles)
    roles["roles"]["advisor-portrait"]["generationPolicy"] = "must-reuse-exact"
    res.append(("re-pinned real likeness advisor-portrait -> must-reuse-exact (valid enum value)", sv.check_asset_roles(roles, CTX.schema)))
    # graph/validator agreement: a rule in prose with no implementation
    g = copy.deepcopy(CTX.graph)
    g["rules"].append({"id": "UNIMPLEMENTED_RULE", "severity": "error", "statement": "x", "exceptions": []})
    errs, _ = sv.validate(EXAMPLE, sv.Ctx(graph=g))
    res.append(("graph rule with no validator implementation", errs))
    # removing the ONE_HERO named exception must break the real not-found template
    g = copy.deepcopy(CTX.graph)
    next(r for r in g["rules"] if r["id"] == "ONE_HERO")["exceptions"] = []
    errs, _ = sv.validate(synth_page("not-found"), sv.Ctx(graph=g))
    res.append(("ONE_HERO exception removed -> real hero-less not-found template rejected", errs))
    return res


def main():
    ok = True
    print("== CONTROLS (expect 0 errors) ==")
    controls = [("example.pagespec.json (home, real copy)", EXAMPLE)]
    controls += [(f"synthesized template '{t}'", synth_page(t)) for t in CTX.templates["templates"]]
    dead = synth_page("not-found"); dead["page"]["route"] = "/give-the-gift"
    controls.append(("dead slug /give-the-gift on not-found template", dead))
    newroute = copy.deepcopy(EXAMPLE); newroute["page"]["route"] = "/new-landing"
    controls.append(("unknown new route /new-landing on home template", newroute))
    for name, spec in controls:
        errors, warns = sv.validate(spec, CTX)
        good = not errors
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] {name}: {len(errors)} errors, {len(warns)} warnings" + (f" -> {errors[:2]}" if errors else ""))
    print("== MUTATIONS (expect rejection) ==")
    for name, fn in CASES:
        errors, _ = sv.validate(fn(), CTX)
        good = bool(errors)
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] {name}: {len(errors)} errors" + (f" | first: {errors[0][:110]}" if errors else ""))
    for name, errors in registry_cases():
        good = bool(errors)
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] {name}: {len(errors)} errors" + (f" | first: {errors[0][:110]}" if errors else ""))
    total = len(controls) + len(CASES) + 5
    print(f"\n{'ALL PASS' if ok else 'FAILURES PRESENT'} ({total} cases: {len(controls)} controls, {len(CASES) + 5} mutations)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
