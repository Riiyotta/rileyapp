#!/usr/bin/env python3
"""Drift proof: every pin / gate / parity check in verify_all.py really catches drift (R5, R9, R10, R14).

Usage:
    python3 extraction/prove_drift.py --scratch DIR      (DIR = an empty or disposable scratch directory)

For each case: copy design-repo/ into DIR/<case>/design-repo, give it the sibling source project (src/, public/
and the CLONE_SPEC / ASSET_MANIFEST / config files are SYMLINKED read-only; package.json and ia.json are copied so a
case may edit them), apply ONE mutation, run that copy's verify_all.py and require exit 1 with the expected
"FAIL [<check>]" tag. The unmutated control copy must exit 0. Nothing outside DIR is written.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.dirname(ROOT)
LINK = ["src", "public", "CLONE_SPEC.md", "CLONE_SPEC_PAGES_BLOG.md", "CLONE_SPEC_PAGES_MARKETING.md", "ASSET_MANIFEST.md", "tailwind.config.js", "index.html"]
COPY = ["package.json", "ia.json"]


def jload(p):
    return json.load(open(p))


def jsave(p, d):
    with open(p, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def edit_json(rel, fn):
    def m(dr):
        p = os.path.join(dr, rel)
        d = jload(p)
        fn(d)
        jsave(p, d)
    return m


def edit_text(rel, old, new):
    def m(dr):
        p = os.path.join(dr, rel)
        s = open(p).read()
        assert old in s, f"{old!r} not in {rel}"
        open(p, "w").write(s.replace(old, new, 1))
    return m


def section(sid, fn):
    return edit_json(f"sections/{sid}.json", fn)


def multi(*ms):
    def m(dr):
        for x in ms:
            x(dr)
    return m


def gate_tpl(t, s, h):
    def fn(d):
        next(x for x in d["sectionHeights"]["templates"][t]["sections"] if x["section"] == s)["height"] = h
    return edit_json("extraction/measured-values.json", fn)


def remove_file(rel):
    return lambda dr: os.remove(os.path.join(dr, rel))


def ia_edit(fn):
    def m(dr):
        p = os.path.join(os.path.dirname(dr), "ia.json")
        d = jload(p)
        fn(d)
        jsave(p, d)
    return m


def first_cite_bump(dr):
    p = os.path.join(dr, "sections", "hero-home.json")
    d = jload(p)
    c = d["implementedBy"][0]["cite"]
    path, rng = c.split(":")
    d["implementedBy"][0]["cite"] = f"{path}:9000"
    jsave(p, d)


CASES = [
    ("asset availability edited in the registry (advisor-portrait -> generation-safe)", edit_json("assets/asset-roles.json", lambda d: d["roles"]["advisor-portrait"].update(availability="generation-safe")), "asset-roles"),
    ("asset generationPolicy re-pinned in the registry (press-logo)", edit_json("assets/asset-roles.json", lambda d: d["roles"]["press-logo"].update(generationPolicy="may-generate-new")), "asset-roles"),
    ("availability pin removed from verify_all.py", edit_text("extraction/verify_all.py", '"press-logo": "blocked-for-generation", ', ""), "asset-roles"),
    ("availability pin loosened in semantic_validate.py", edit_text("schema/semantic_validate.py", '"press-logo": "blocked-for-generation"', '"press-logo": "generation-safe"'), "asset-roles"),
    ("retrieval flipped in contract AND allowlist together", multi(section("cookie-consent", lambda d: d.update(retrievalEligible=True)),
                                                                  edit_json("tokens/llm/component-allowlist.json", lambda d: d.update(retrievalIneligible=[]))), "retrieval"),
    ("retrieval pin removed from semantic_validate.py", edit_text("schema/semantic_validate.py", 'RETRIEVAL_INELIGIBLE = {"cookie-consent"}', "RETRIEVAL_INELIGIBLE = set()"), "retrieval"),
    ("content section marked retrieval-ineligible", section("blog-post-grid", lambda d: d.update(retrievalEligible=False, retrievalReason="x" * 40)), "retrieval"),
    ("runtime component un-pinned (mobile-menu eligible)", edit_json("components/mobile-menu.json", lambda d: d.update(retrievalEligible=True)), "retrieval"),
    ("phantom allowlist section", edit_json("tokens/llm/component-allowlist.json", lambda d: d["sections"].append("hero-video")), "allowlist"),
    ("citation pushed out of range", first_cite_bump, "citations"),
    ("citation anchor no longer in range", section("final-cta", lambda d: d["implementedBy"][0].update(anchor="not in this file")), "citations"),
    ("manifest count hand-edited", edit_json("registry.manifest.json", lambda d: d["counts"].update(sections=99)), "counts"),
    ("README counts marker stale", edit_text("README.md", '"sections":36', '"sections":35'), "readme-counts"),
    ("allowlist version bumped alone", edit_json("tokens/llm/component-allowlist.json", lambda d: d.update(version="9.9.9")), "versions"),
    ("token catalog value hand-edited", edit_json("tokens/llm/token-catalog.json", lambda d: d["tokens"]["tokens.00-foundation.color.tokens.ink"].update(value="#000001")), "token-catalog"),
    ("token file changed without rebuilding the catalog", edit_json("tokens/00-foundation/color.json", lambda d: d["tokens"].update(invented={"value": "#123456"})), "token-catalog"),
    ("token policy property map drifts from validator", edit_json("tokens/llm/token-policy.json", lambda d: d["propertyCategories"].update(spacing=["color-roles"])), "token-catalog"),
    ("leakage registry: shingle removed", edit_json("schema/leakage-patterns.json", lambda d: d["copyShingles"]["hashes"].pop()), "leakage"),
    ("leakage registry: persons emptied", edit_json("schema/leakage-patterns.json", lambda d: d.update(persons=[])), "leakage"),
    ("leakage registry claims human review", edit_json("schema/leakage-patterns.json", lambda d: d.update(humanReviewed=True)), "leakage"),
    ("validator edited without re-binding the policy hash", edit_text("schema/semantic_validate.py", "MARQUEE_PATTERNS = {", "# drift\nMARQUEE_PATTERNS = {"), "policy"),
    ("manifest binds the SaaS common policy", edit_json("registry.manifest.json", lambda d: d["designPolicy"].update(policyId="n0-saas-design-constraints-common")), "policy"),
    ("policy says isSaaS true", edit_json("policy/design-policy.json", lambda d: d["classification"].update(isSaaS=True)), "policy"),
    ("manifest category set to saas", edit_json("registry.manifest.json", lambda d: d.update(category="saas")), "policy"),
    ("wrapper-gate HERO threshold loosened in code", edit_text("extraction/wrapper_gate.py", "HERO_ERROR_PX = 3000", "HERO_ERROR_PX = 9000"), "wrapper-gate"),
    ("wrapper-gate share threshold loosened in code", edit_text("extraction/wrapper_gate.py", "SHARE_ERROR = 0.60", "SHARE_ERROR = 0.95"), "wrapper-gate"),
    ("measured HERO 3100px (not whitelisted)", gate_tpl("pricing", "pricing-hero", 3100), "wrapper-gate"),
    ("measured whole-page section (blog grid 4000px)", gate_tpl("blog-index", "blog-post-grid", 4000), "wrapper-gate"),
    ("template measurement removed", edit_json("extraction/measured-values.json", lambda d: d["sectionHeights"]["templates"].pop("legal")), "wrapper-gate"),
    ("semantic.id diverges from contract id", section("article-header", lambda d: d["semantic"].update(id="hero")), "provenance"),
    ("source.lines shifted off the tag", section("article-toc", lambda d: d["source"].update(lines="1-5")), "provenance"),
    ("source.id equal to semantic id", section("blog-search", lambda d: d["source"].update(id="blog-search")), "section-schema"),
    ("section contract gains an unknown property", section("legal-policy-embed", lambda d: d.update(wholePage=True)), "section-schema"),
    ("article route dropped from the route table", edit_json("templates/templates.json", lambda d: d.update(routes=[r for r in d["routes"] if r["path"] != "/blog/sleep/baby-witching-hour"])), "routes"),
    ("route mapped twice", edit_json("templates/templates.json", lambda d: d["routes"].append({"path": "/pricing", "template": "home"})), "routes"),
    ("unbuilt link re-bound to a content template", edit_json("templates/templates.json", lambda d: next(r for r in d["routes"] if r["path"] == "/blog/authors").update(template="blog-index")), "routes"),
    ("generated example leaks the Riley brand", edit_json("schema/examples/home.generated.pagespec.json", lambda d: d["nodes"][2]["content"].update(heading="Meet Riley")), "examples"),
    ("family loses its generation-safe example", remove_file("schema/examples/legal.generated.pagespec.json"), "examples"),
    ("graph rule removed", edit_json("compatibility/graph.json", lambda d: d.update(rules=[r for r in d["rules"] if r["id"] != "GENERATION_MODE_COPY"])), "graph"),
    ("motion-spec forgets a section", edit_json("animation/motion-spec.json", lambda d: d["patterns"]["sticky-aside"].update(sections=[])), "motion"),
    ("ia.json loses a section the design-repo maps", ia_edit(lambda d: d["sections"].pop("article.chapter")), "ia"),
    ("absolute machine path injected", edit_text("README.md", "# ", "# see " + "/" + "Users" + "/someone/x\n# ", ), "abs-paths"),
    ("whitelist entry without agent attestation", edit_json("extraction/wrapper-whitelist.json", lambda d: d.update(entries=[{"template": "pricing", "section": "pricing-hero", "maxHeightPx": 4000, "justification": "a long enough justification text here", "reviewedBy": "agent"}])), "wrapper-gate"),
]


def make_copy(base, name):
    case_dir = os.path.join(base, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60])
    if os.path.exists(case_dir):
        shutil.rmtree(case_dir)
    os.makedirs(case_dir)
    dr = os.path.join(case_dir, "design-repo")
    shutil.copytree(ROOT, dr, ignore=shutil.ignore_patterns("__pycache__", "*.zip", ".DS_Store"))
    for x in LINK:
        if os.path.exists(os.path.join(SRC, x)):
            os.symlink(os.path.join(SRC, x), os.path.join(case_dir, x))
    for x in COPY:
        if os.path.exists(os.path.join(SRC, x)):
            shutil.copy(os.path.join(SRC, x), os.path.join(case_dir, x))
    return dr


def run(dr):
    r = subprocess.run([sys.executable, os.path.join(dr, "extraction", "verify_all.py")], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    base = os.path.abspath(ap.parse_args().scratch)
    os.makedirs(base, exist_ok=True)
    if not os.path.isdir(os.path.join(SRC, "src")):
        print("source project absent: drift proof needs the sibling clone (src/, public/)")
        return 1
    ok = True
    dr = make_copy(base, "control")
    code, out = run(dr)
    good = code == 0
    ok &= good
    print(f"[{'PASS' if good else 'FAIL'}] control (unmodified copy) exits 0" + ("" if good else "\n" + out[-800:]))
    for name, mutate, tag in CASES:
        dr = make_copy(base, name)
        mutate(dr)
        code, out = run(dr)
        hit = f"FAIL [{tag}]" in out
        good = code == 1 and hit
        ok &= good
        first = next((l for l in out.splitlines() if l.startswith(f"FAIL [{tag}]")), "")
        print(f"[{'PASS' if good else 'FAIL'}] {name} -> [{tag}] {first[len(tag) + 8:][:100]}" + ("" if good else f"\n    exit {code}; fails: {[l for l in out.splitlines() if l.startswith('FAIL')][:3]}"))
    print(f"\n{'ALL DRIFT CAUGHT' if ok else 'DRIFT NOT CAUGHT'} ({len(CASES)} drift cases + 1 control)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
