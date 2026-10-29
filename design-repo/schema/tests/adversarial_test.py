#!/usr/bin/env python3
"""Adversarial suite for the Riley-clone PageSpec contract (pageSpecVersion 2.0.0).

Usage: python3 schema/tests/adversarial_test.py        (needs jsonschema)

CONTROLS (must produce zero errors):
  * every schema/examples/*.pagespec.json (8 clone examples with REAL clone content, 7 generation examples)
  * one clone-mode AND one generation-mode PageSpec auto-synthesized per template from the schema + template node
    list (a new template is covered with no new code)
  * a dead sitemap slug and an unbuilt author link bound to not-found; valid node.style tokens
MUTATIONS (each must be rejected with >=1 error from the NAMED rule, or a schema error where noted).
WRAPPER-GATE cases exercise extraction/wrapper_gate.py with mutated measurements / whitelists.
Exit 0 only if every control passes and every mutation is rejected as expected.
Root derived from __file__ (no absolute paths).
"""
import copy
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "schema"))
sys.path.insert(0, os.path.join(ROOT, "extraction"))
import semantic_validate as sv  # noqa: E402
import wrapper_gate  # noqa: E402

CTX = sv.Ctx()
EX = {os.path.basename(p).replace(".pagespec.json", ""): json.load(open(p)) for p in sorted(glob.glob(os.path.join(ROOT, "schema/examples/*.pagespec.json")))}
ROLES = CTX.roles["roles"]


# ------------------------------------------------------------------ generic synthesizer
def synth(sch, mode):
    if "$ref" in sch:
        return synth(CTX.schema["definitions"][sch["$ref"].split("/")[-1]], mode)
    if "const" in sch:
        return copy.deepcopy(sch["const"])
    if "enum" in sch:
        return sch["enum"][0]
    t = sch.get("type")
    if t == "object":
        props = sch["properties"]
        out = {k: synth(props[k], mode) for k in sch.get("required", [])}
        if "assetRole" in out:
            enum = props["assetRole"]["enum"]
            if mode == "generation":
                out["assetRole"] = next(r for r in enum if ROLES[r]["availability"] == "generation-safe" and r != "placeholder-url") \
                    if any(ROLES[r]["availability"] == "generation-safe" and r != "placeholder-url" for r in enum) else "placeholder-url"
            if "assetRef" in out:
                role = ROLES[out["assetRole"]]
                out["assetRef"] = role["files"][0] if (mode == "clone" and role.get("files")) else "generated:placeholder"
            if out["assetRole"] == "placeholder-url":
                out["href"] = "https://site.example/"
        return out
    if t == "array":
        return [synth(sch["items"], mode) for _ in range(sch.get("minItems", 0))]
    if t == "boolean":
        return False
    if t == "integer":
        return sch.get("minimum", 0)
    if t == "string":
        return "Placeholder"
    raise ValueError(f"cannot synthesize {sch}")


def synth_page(tname, mode="clone"):
    tpl = CTX.templates["templates"][tname]
    route = next(r["path"] for r in CTX.templates["routes"] if r["template"] == tname) if mode == "clone" else f"/synth-{tname}"
    nodes = []
    for tn in tpl["nodes"]:
        if not tn["required"]:
            continue
        sid, var = tn["section"], tn.get("variant")
        dn = f"node_{sid}__{var}" if var and f"node_{sid}__{var}" in CTX.schema["definitions"] else f"node_{sid}"
        n = synth(CTX.schema["definitions"][dn], mode)
        if var:
            n["variant"] = var
        nodes.append(n)
    page = {"route": route, "title": "Placeholder", "template": tname, "mode": mode, "theme": "riley-light"}
    if mode == "generation":
        page["brand"] = {"name": "Sample Co"}
    return {"pageSpecVersion": "2.0.0", "page": page, "nodes": nodes}


# ------------------------------------------------------------------ helpers
def ex(name):
    return copy.deepcopy(EX[name])


def find(spec, t, k=0):
    return [n for n in spec["nodes"] if n["type"] == t][k]


def idx(spec, t):
    return next(i for i, n in enumerate(spec["nodes"]) if n["type"] == t)


def gen(name, f):
    s = ex(f"{name}.generated")
    f(s)
    return s


def clone(name, f):
    s = ex(f"{name}.clone")
    f(s)
    return s


def setc(t, key, val, name="home", k=0):
    def f(s):
        find(s, t, k)["content"][key] = val
    return f


def hero_heading(val):
    return gen("home", setc("hero-home", "heading", val))


def style(prop, val):
    def f(s):
        find(s, "hero-home")["style"] = {prop: val}
    return gen("home", f)


SRC_QUOTE = EX["home.clone"]["nodes"][9]["content"]["slides"][1]["quote"]
SRC_EXCERPT = EX["blog-index.clone"]["nodes"][5]["content"]["excerpt"]

# (label, spec, expected rule-id prefix or "SCHEMA")
CASES = [
    # ---------------- generation-mode leakage (R2)
    ("brand in hero heading", lambda: hero_heading("Meet Riley today"), "GENERATION_MODE_BRAND"),
    ("brand letter-spaced R.i.l.e.y", lambda: hero_heading("Say hi to R.i.l.e.y"), "GENERATION_MODE_BRAND"),
    ("brand with zero-width joiner", lambda: hero_heading("Ri​ley helps"), "GENERATION_MODE_BRAND"),
    ("brand with Cyrillic homoglyph", lambda: hero_heading("Rіley helps"), "GENERATION_MODE_BRAND"),
    ("brand product name 'Riley Plus+'", lambda: gen("pricing", lambda s: find(s, "pricing-hero")["content"]["plans"][0].update(name="Riley Plus+")), "GENERATION_MODE_BRAND"),
    ("brand feature name 'Golden Window'", lambda: hero_heading("Try Golden Window"), "GENERATION_MODE_BRAND"),
    ("generation page without page.brand", lambda: gen("home", lambda s: s["page"].pop("brand")), "GENERATION_MODE_BRAND"),
    ("page.brand named Riley", lambda: gen("home", lambda s: s["page"]["brand"].update(name="Riley")), "GENERATION_MODE_BRAND"),
    ("clone page carrying page.brand", lambda: clone("home", lambda s: s["page"].update(brand={"name": "X"})), "GENERATION_MODE_BRAND"),
    ("Riley wordmark logo in generation", lambda: gen("home", lambda s: find(s, "site-header")["content"].update(logo={"assetRole": "brand-wordmark", "assetRef": "/assets/wordmark.svg", "alt": "Logo"})), "GENERATION_MODE_ASSET"),
    ("real source file on a generation-safe role", lambda: gen("home", lambda s: find(s, "final-cta")["content"].update(background={"assetRole": "decorative-cloud", "assetRef": "/assets/background-clouds(1).svg"})), "GENERATION_MODE_ASSET"),
    ("Riley mascot in generation", lambda: gen("home", lambda s: find(s, "final-cta")["content"].update(mascots={"assetRole": "mascot-illustration", "assetRef": "/assets/mascots.svg"})), "GENERATION_MODE_ASSET"),
    ("article cover photo (real child imagery)", lambda: gen("blog-article", lambda s: find(s, "article-header")["content"].update(cover={"assetRole": "article-cover-photo", "assetRef": "/assets/blog/baby-witching-hour.jpg", "alt": "x"})), "GENERATION_MODE_ASSET"),
    ("App Store badge role", lambda: gen("home", lambda s: find(s, "site-footer")["content"]["app"]["badge"].update(assetRole="store-badge", assetRef="/assets/icons/app-store-badge.svg")), "GENERATION_MODE_STORE"),
    ("store wording 'Download on the App Store'", lambda: gen("home", lambda s: find(s, "site-footer")["content"]["app"].update(heading="Download on the App Store")), "GENERATION_MODE_STORE"),
    ("app-store OneLink role on CTA", lambda: gen("home", lambda s: find(s, "final-cta")["content"].update(cta={"label": "Get it", "assetRole": "app-store-onelink"})), "GENERATION_MODE_STORE"),
    ("store link text rileyapp.onelink.me", lambda: hero_heading("Get it at rileyapp.onelink.me now"), "GENERATION_MODE_URL"),
    ("real review quote", lambda: gen("home", lambda s: find(s, "testimonials-carousel")["content"]["slides"][0].update(quote=SRC_QUOTE)), "GENERATION_MODE_COPY"),
    ("rating wording", lambda: hero_heading("Rated 4.9 stars"), "GENERATION_MODE_RATING"),
    ("review count", lambda: hero_heading("Over 12,000 reviews"), "GENERATION_MODE_RATING"),
    ("source review heading", lambda: gen("home", setc("testimonials-carousel", "eyebrow", "Real Reviews, Real Families")), "GENERATION_MODE_RATING"),
    ("real clinician name", lambda: gen("home", lambda s: find(s, "clinical-board")["content"]["advisors"][0].update(name="Dr. Kate Roche")), "GENERATION_MODE_PERSON"),
    ("real author byline", lambda: gen("blog-article", lambda s: find(s, "article-header")["content"]["bylines"][0].update(name="Sam Fore")), "GENERATION_MODE_PERSON"),
    ("real testimonial attribution", lambda: gen("home", lambda s: find(s, "testimonials-carousel")["content"]["slides"][0].update(attribution="Max L., Dad of Baby R (1 mo)")), "GENERATION_MODE_PERSON"),
    ("real clinician portrait role", lambda: gen("home", lambda s: find(s, "clinical-board")["content"]["advisors"][0].update(portrait={"assetRole": "advisor-portrait", "assetRef": "/assets/kate.png", "alt": "x"})), "GENERATION_MODE_PERSON"),
    ("real author avatar role", lambda: gen("blog-article", lambda s: find(s, "article-header")["content"]["bylines"][0].update(avatar={"assetRole": "author-avatar", "assetRef": "/assets/blog/authors/sam-fore.png", "alt": "x"})), "GENERATION_MODE_PERSON"),
    ("real user-story photo role", lambda: gen("home", lambda s: find(s, "featurette-carousel")["content"]["slides"][0].update(photo={"assetRole": "user-story-photo", "assetRef": "/assets/meg.png", "alt": "x"})), "GENERATION_MODE_PERSON"),
    ("press outlet name", lambda: hero_heading("As seen in TechCrunch"), "GENERATION_MODE_CUSTOMER"),
    ("real press logo role", lambda: gen("home", lambda s: find(s, "press-marquee")["content"]["logos"][0].update(assetRole="press-logo", assetRef="/assets/nbc.png")), "GENERATION_MODE_CUSTOMER"),
    ("real competitor in comparison table", lambda: gen("pricing", lambda s: find(s, "gradient-band")["content"]["comparisonTable"]["columns"][1].update(label="ChatGPT")), "GENERATION_MODE_CUSTOMER"),
    ("social platform mark role", lambda: gen("blog-article", lambda s: find(s, "article-share-row")["content"]["share"]["platforms"][0].update(icon={"assetRole": "social-share-mark", "assetRef": "/assets/blog/icons/share-x.svg"})), "GENERATION_MODE_CUSTOMER"),
    ("Riley domain in copy", lambda: hero_heading("Visit rileyapp.com/pricing"), "GENERATION_MODE_URL"),
    ("non-reserved URL in copy", lambda: hero_heading("See https://example.com/a"), "GENERATION_MODE_URL"),
    ("href on a non-reserved host (schema)", lambda: gen("home", lambda s: find(s, "final-cta")["content"]["cta"].update(href="https://evil.com/x")), "SCHEMA"),
    ("real Riley article route", lambda: gen("blog-article", lambda s: s["page"].update(route="/blog/sleep/baby-witching-hour")), "GENERATION_MODE_URL"),
    ("newsletter live endpoint role", lambda: gen("home", lambda s: find(s, "site-footer")["content"]["newsletter"].update(assetRole="newsletter-endpoint")), "GENERATION_MODE_URL"),
    ("source blog excerpt", lambda: gen("blog-index", lambda s: find(s, "blog-featured-banner")["content"].update(excerpt=SRC_EXCERPT)), "GENERATION_MODE_COPY"),
    ("source copy with curly quotes + em dash", lambda: hero_heading("We are raising a generation—of confident parents"), "GENERATION_MODE_COPY"),
    ("source CTA", lambda: gen("home", lambda s: find(s, "final-cta")["content"]["cta"].update(label="Get support that gets you")), "GENERATION_MODE_COPY"),
    ("source health claim", lambda: hero_heading("Pediatrician-backed answers"), "GENERATION_MODE_CLAIM"),
    ("policy health claim", lambda: hero_heading("Clinically proven better sleep"), "GENERATION_MODE_CLAIM"),
    ("SIDS safety claim", lambda: gen("blog-article", lambda s: find(s, "article-intro")["content"]["blocks"][0].update(text="This routine prevents SIDS.")), "GENERATION_MODE_CLAIM"),
    ("source price claim", lambda: gen("pricing", lambda s: find(s, "pricing-hero")["content"]["plans"][0]["price"].update(amount="$9.99")), "GENERATION_MODE_CLAIM"),
    ("source citation role in generation", lambda: gen("blog-article", lambda s: find(s, "article-sources")["content"].update(summaryLabel="1 source", sources=[{"citation": "A study", "link": {"assetRole": "source-citation"}}])), "GENERATION_MODE_CLAIM"),
    ("Rive chat screen role", lambda: gen("home", lambda s: find(s, "featurette-carousel")["content"]["slides"][0].update(rive={"assetRole": "rive-animation", "assetRef": "/assets/animations/chat_module_meg.riv", "artboard": "x", "stateMachine": "y"})), "GENERATION_MODE_SCREENSHOT"),
    ("Rive artboard identifier", lambda: gen("home", lambda s: find(s, "featurette-carousel")["content"]["slides"][0]["rive"].update(artboard="chat_module_meg")), "GENERATION_MODE_SCREENSHOT"),
    ("policy-embed role in generation", lambda: gen("legal", lambda s: find(s, "legal-policy-embed")["content"].update(embed={"assetRole": "policy-embed"})), "GENERATION_MODE_EMBED"),
    ("policy-embed id in generation", lambda: gen("legal", lambda s: find(s, "legal-policy-embed")["content"]["embed"].update(embedId="1b687b5a-20d7-48f3-be50-cae504edce40")), "GENERATION_MODE_EMBED"),
    # ---------------- clone-mode asset rules
    ("clone: unregistered file for must-not-fabricate role", lambda: clone("home", lambda s: find(s, "clinical-board")["content"]["advisors"][0]["portrait"].update(assetRef="/assets/generated-doctor.png")), "REGISTERED_ASSET_REF"),
    ("clone: generated: ref for press logo", lambda: clone("home", lambda s: find(s, "press-marquee")["content"]["logos"][0].update(assetRef="generated:new")), "REGISTERED_ASSET_REF"),
    ("clone: unregistered /assets file on a generic role", lambda: clone("home", lambda s: find(s, "final-cta")["content"]["background"].update(assetRef="/assets/invented.svg")), "REGISTERED_ASSET_REF"),
    ("href on a non placeholder-url role", lambda: clone("home", lambda s: find(s, "final-cta")["content"]["cta"].update(href="https://site.example/")), "PLACEHOLDER_HREF_ROLE"),
    ("placeholder-url without href", lambda: gen("home", lambda s: find(s, "final-cta")["content"]["cta"].pop("href")), "PLACEHOLDER_HREF_ROLE"),
    ("invented assetRole (schema)", lambda: clone("home", lambda s: find(s, "clinical-board")["content"]["advisors"][0]["portrait"].update(assetRole="stock-photo")), "SCHEMA"),
    # ---------------- mode / schema
    ("mode missing (schema)", lambda: clone("home", lambda s: s["page"].pop("mode")), "SCHEMA"),
    ("mode 'reference' not in closed enum (schema)", lambda: clone("home", lambda s: s["page"].update(mode="reference")), "SCHEMA"),
    ("legacy brandContext field (schema)", lambda: clone("home", lambda s: s["page"].update(brandContext="riley-clone")), "SCHEMA"),
    ("old pageSpecVersion (schema)", lambda: clone("home", lambda s: s.update(pageSpecVersion="1.0.0")), "SCHEMA"),
    ("invented section type (schema)", lambda: clone("home", lambda s: s["nodes"].insert(3, {"type": "hero-video", "content": {}, "motion": {"pattern": "static", "reducedMotionFallback": "x"}})), "SCHEMA"),
    ("invented motion field (schema)", lambda: clone("home", lambda s: find(s, "clinical-board")["motion"].update(scrollReveal="fade-up")), "SCHEMA"),
    ("wrong motion pattern for section (schema)", lambda: clone("blog-article", lambda s: find(s, "article-toc")["motion"].update(pattern="static")), "SCHEMA"),
    ("missing reducedMotionFallback (schema)", lambda: clone("home", lambda s: find(s, "faq-clouds")["motion"].pop("reducedMotionFallback")), "SCHEMA"),
    # ---------------- structure / templates / routes
    ("template/node mismatch (home nodes as pricing)", lambda: clone("home", lambda s: s["page"].update(template="pricing", route="/pricing")), "TEMPLATE_NODE_SEQUENCE"),
    ("removed required node (article-sources)", lambda: clone("blog-article", lambda s: s["nodes"].pop(idx(s, "article-sources"))), "TEMPLATE_NODE_SEQUENCE"),
    ("article with zero chapters", lambda: clone("blog-article", lambda s: s.update(nodes=[n for n in s["nodes"] if n["type"] != "article-chapter"])), "TEMPLATE_NODE_SEQUENCE"),
    ("text-page chapter after closing", lambda: clone("text-page", lambda s: s["nodes"].insert(len(s["nodes"]) - 1, copy.deepcopy(find(s, "text-page-chapter")))), "TEMPLATE_NODE_SEQUENCE"),
    ("announcement bar added to article", lambda: clone("blog-article", lambda s: s["nodes"].insert(0, copy.deepcopy(EX["home.clone"]["nodes"][0]))), "TEMPLATE_NODE_SEQUENCE"),
    ("whole-article single chapter duplicated as intro (one-per-page)", lambda: clone("blog-article", lambda s: s["nodes"].insert(idx(s, "article-intro"), copy.deepcopy(find(s, "article-intro")))), "ONE_PER_PAGE"),
    ("reordered footer before final-cta", lambda: clone("blog-index", lambda s: s["nodes"].insert(idx(s, "final-cta"), s["nodes"].pop(idx(s, "site-footer")))), "FOOTER_LAST"),
    ("site-header standalone before hero-home", lambda: clone("home", lambda s: find(s, "site-header").update(variant="standalone")), "HEADER_VARIANT_BINDING"),
    ("dead slug bound to home", lambda: clone("home", lambda s: s["page"].update(route="/baby-tracker")), "ROUTE_TEMPLATE_BINDING"),
    ("unbuilt author link bound to blog-index", lambda: clone("blog-index", lambda s: s["page"].update(route="/blog/author/sam-fore")), "ROUTE_TEMPLATE_BINDING"),
    ("article route bound to text-page", lambda: clone("text-page", lambda s: s["page"].update(route="/blog/sleep/baby-witching-hour")), "ROUTE_TEMPLATE_BINDING"),
    ("TOC does not match chapters", lambda: clone("blog-article", lambda s: find(s, "article-toc")["content"]["entries"].pop()), "TOC_MATCHES_CHAPTERS"),
    ("citation without a source", lambda: clone("blog-article", lambda s: find(s, "article-intro")["content"]["blocks"][0].update(citations=[9])), "ARTICLE_CITATIONS_RESOLVE"),
    ("list block without items", lambda: clone("blog-article", lambda s: find(s, "article-chapter")["content"]["blocks"].append({"kind": "list", "text": "x"})), "ARTICLE_BLOCK_SHAPE"),
    ("paragraph block carrying an image", lambda: clone("blog-article", lambda s: find(s, "article-chapter")["content"]["blocks"][0].update(image=find(s, "article-header")["content"]["cover"])), "ARTICLE_BLOCK_SHAPE"),
    ("pagination page beyond total", lambda: clone("blog-index", lambda s: find(s, "blog-pagination")["content"].update(page=40)), "PAGINATION_BOUNDS"),
    ("category listing with several pages", lambda: clone("blog-category", lambda s: find(s, "blog-pagination")["content"].update(totalPages=3)), "PAGINATION_BOUNDS"),
    ("active tab out of range", lambda: clone("blog-index", lambda s: find(s, "blog-category-tabs")["content"].update(activeIndex=9)), "PAGINATION_BOUNDS"),
    ("maxWords overflow (article title 30 words)", lambda: clone("blog-article", lambda s: find(s, "article-header")["content"].update(title=" ".join(["word"] * 30))), "MAX_WORDS"),
    ("maxWords overflow nested (block text 90 words)", lambda: clone("blog-article", lambda s: find(s, "article-chapter")["content"]["blocks"][0].update(text=" ".join(["word"] * 90))), "MAX_WORDS"),
    ("comparison matrix shape", lambda: clone("pricing", lambda s: find(s, "gradient-band")["content"]["comparisonTable"]["rows"][0]["marks"].pop()), "COMPARISON_MATRIX_SHAPE"),
    # ---------------- retrieval eligibility (R8), node level
    ("cookie-consent placed in nodes[]", lambda: clone("legal", lambda s: s["nodes"].insert(3, copy.deepcopy(s["overlays"][0]))), "RETRIEVAL_INELIGIBLE_NODE"),
    ("content section in overlays[] (schema)", lambda: clone("legal", lambda s: s["overlays"].append(copy.deepcopy(find(s, "legal-policy-embed")))), "SCHEMA"),
    # ---------------- tokens (R10)
    ("raw hex colour", lambda: style("surface", "#ff00aa"), "TOKEN_RAW_COLOR"),
    ("raw rgb colour", lambda: style("text", "rgb(10, 20, 30)"), "TOKEN_RAW_COLOR"),
    ("raw oklch colour", lambda: style("accent", "oklch(70% 0.1 200)"), "TOKEN_RAW_COLOR"),
    ("arbitrary px spacing", lambda: style("spacing", "24px"), "TOKEN_ARBITRARY_SPACING"),
    ("arbitrary rem radius", lambda: style("radius", "1.5rem"), "TOKEN_ARBITRARY_SPACING"),
    ("unsupported font", lambda: style("fontFamily", "Comic Sans MS"), "TOKEN_UNSUPPORTED_FONT"),
    ("unknown token path", lambda: style("surface", "tokens.10-semantic.color-roles.roles.surface.neon"), "TOKEN_UNKNOWN"),
    ("token of the wrong category for the property", lambda: style("spacing", "tokens.10-semantic.color-roles.roles.surface.card"), "TOKEN_THEME_COMBINATION"),
    ("token of another theme", lambda: style("surface", "tokens.themes.riley-dark.surface.page"), "TOKEN_THEME_COMBINATION"),
]


def registry_cases():
    res = []

    def roles_mut(f):
        r = copy.deepcopy(CTX.roles)
        f(r["roles"])
        return sv.check_asset_roles(r, CTX.schema)
    res.append(("re-pin press-logo policy -> may-generate-new (valid value)", roles_mut(lambda R: R["press-logo"].update(generationPolicy="may-generate-new"))))
    res.append(("availability advisor-portrait -> generation-safe (valid value)", roles_mut(lambda R: R["advisor-portrait"].update(availability="generation-safe"))))
    res.append(("availability brand-wordmark -> generation-safe (real mark)", roles_mut(lambda R: R["brand-wordmark"].update(availability="generation-safe"))))
    res.append(("availability store-badge -> clone-only (valid value, wrong pin)", roles_mut(lambda R: R["store-badge"].update(availability="clone-only"))))
    res.append(("blocked role with no substitutes", roles_mut(lambda R: R["press-logo"].update(generationSafeSubstitutes=[]))))
    res.append(("substitute that is not generation-safe", roles_mut(lambda R: R["press-logo"].update(generationSafeSubstitutes=["brand-wordmark"]))))
    res.append(("availability outside the closed set", roles_mut(lambda R: R["ui-icon"].update(availability="reference-only"))))
    secs = copy.deepcopy(CTX.sections)
    secs["cookie-consent"]["retrievalEligible"] = True
    res.append(("contract: cookie-consent flipped to retrievalEligible", sv.check_retrieval(secs)))
    secs = copy.deepcopy(CTX.sections)
    secs["blog-post-grid"]["retrievalEligible"] = False
    secs["blog-post-grid"]["retrievalReason"] = "x" * 40
    res.append(("contract: content section marked retrieval-ineligible", sv.check_retrieval(secs)))
    secs = copy.deepcopy(CTX.sections)
    secs["promo-modal"] = dict(copy.deepcopy(secs["blog-pagination"]), id="promo-modal", retrievalEligible=True)
    res.append(("contract: runtime-UI-looking section left eligible", sv.check_retrieval(secs)))
    g = copy.deepcopy(CTX.graph)
    g["rules"].append({"id": "UNIMPLEMENTED_RULE", "severity": "error", "statement": "x", "exceptions": []})
    res.append(("graph rule with no validator implementation", sv.validate(EX["home.clone"], sv.Ctx(graph=g))[0]))
    g = copy.deepcopy(CTX.graph)
    next(r for r in g["rules"] if r["id"] == "ONE_HERO")["exceptions"] = []
    res.append(("ONE_HERO exceptions removed -> real hero-less legal template rejected", sv.validate(EX["legal.clone"], sv.Ctx(graph=g))[0]))
    return res


def gate_cases():
    base = json.load(open(os.path.join(ROOT, "extraction/measured-values.json")))
    wl0 = {"entries": []}
    out = []

    def mv(f):
        m = copy.deepcopy(base)
        f(m["sectionHeights"])
        return m

    def sec(m, t, s):
        return next(x for x in m["templates"][t]["sections"] if x["section"] == s)
    e, w = wrapper_gate.run(mv(lambda m: sec(m, "pricing", "pricing-hero").update(height=1900)), wl0)
    out.append(("HERO 1900px -> warn only", (not e) and any("1800" in x for x in w)))
    e, w = wrapper_gate.run(mv(lambda m: sec(m, "pricing", "pricing-hero").update(height=3100)), wl0)
    out.append(("HERO 3100px -> error", bool(e)))
    wl = {"entries": [{"template": "pricing", "section": "pricing-hero", "maxHeightPx": 3200, "justification": "reviewed tall plan hero for a test fixture case",
                       "reviewedBy": "adversarial fixture (agent attestation, not a human sign-off)"}]}
    e, w = wrapper_gate.run(mv(lambda m: sec(m, "pricing", "pricing-hero").update(height=3100)), wl)
    out.append(("HERO 3100px whitelisted -> no error but still warns", (not e) and bool(w)))
    e, w = wrapper_gate.run(mv(lambda m: sec(m, "blog-index", "blog-post-grid").update(height=4000)), wl0)
    out.append(("one section > 60% of its page -> error", bool(e)))
    e, w = wrapper_gate.run(mv(lambda m: sec(m, "blog-index", "blog-post-grid").update(height=2700)), wl0)
    out.append(("one section 50-60% of its page -> warn only", (not e) and bool(w)))
    e, w = wrapper_gate.run(mv(lambda m: m["templates"].pop("blog-article")), wl0)
    out.append(("missing template measurement -> error", bool(e)))
    e, w = wrapper_gate.run(mv(lambda m: m["templates"]["text-page"].update(sections=[x for x in m["templates"]["text-page"]["sections"] if x["section"] != "text-page-closing"])), wl0)
    out.append(("missing required section measurement -> error", bool(e)))
    e, w = wrapper_gate.run(mv(lambda m: m.update(viewport=1024)), wl0)
    out.append(("measured at the wrong viewport -> error", bool(e)))
    bad = copy.deepcopy(wl)
    bad["entries"][0]["justification"] = "short"
    e, w = wrapper_gate.run(mv(lambda m: sec(m, "pricing", "pricing-hero").update(height=3100)), bad)
    out.append(("whitelist without 30-char justification -> error", bool(e)))
    bad = copy.deepcopy(wl)
    bad["entries"][0]["reviewedBy"] = "review agent"
    e, w = wrapper_gate.run(mv(lambda m: sec(m, "pricing", "pricing-hero").update(height=3100)), bad)
    out.append(("agent whitelist without attestation wording -> error", bool(e)))
    e, w = wrapper_gate.run(base, wl)
    out.append(("stale whitelist entry -> error", bool(e)))
    return out


def main():
    ok = True
    print("== CONTROLS (expect 0 errors) ==")
    controls = [(f"example {k}", v) for k, v in EX.items()]
    controls += [(f"synthesized clone '{t}'", synth_page(t)) for t in CTX.templates["templates"]]
    controls += [(f"synthesized generation '{t}'", synth_page(t, "generation")) for t in CTX.templates["templates"]]
    dead = synth_page("not-found"); dead["page"]["route"] = "/give-the-gift"
    controls.append(("dead slug /give-the-gift on not-found", dead))
    unb = synth_page("not-found"); unb["page"]["route"] = "/blog/author/sam-fore"
    controls.append(("unbuilt link /blog/author/sam-fore on not-found", unb))
    st = ex("home.generated")
    find(st, "hero-home")["style"] = {"surface": "tokens.10-semantic.color-roles.roles.surface.lilac", "spacing": "tokens.30-layout.section-spacing.tokens.featurette",
                                      "fontFamily": "tokens.00-foundation.typography.families.serif", "radius": "tokens.00-foundation.radius.tokens.card"}
    controls.append(("valid node.style token references", st))
    for name, spec in controls:
        errors, warns = sv.validate(spec, CTX)
        good = not errors
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] {name}: {len(errors)} errors, {len(warns)} warnings" + (f" -> {errors[:2]}" if errors else ""))
    print("== MUTATIONS (expect rejection by the named rule) ==")
    for name, fn, want in CASES:
        errors, _ = sv.validate(fn(), CTX)
        hit = [e for e in errors if e.startswith(want)]
        good = bool(hit)
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] {name}: {want} x{len(hit)}" + (f" | {hit[0][:110]}" if hit else f" | got {errors[:1]}"))
    print("== REGISTRY MUTATIONS ==")
    reg = registry_cases()
    for name, errors in reg:
        good = bool(errors)
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] {name}: {len(errors)} errors" + (f" | {errors[0][:110]}" if errors else ""))
    print("== WRAPPER GATE ==")
    gc = gate_cases()
    for name, good in gc:
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] {name}")
    total = len(controls) + len(CASES) + len(reg) + len(gc)
    print(f"\n{'ALL PASS' if ok else 'FAILURES PRESENT'} ({total} cases: {len(controls)} controls, {len(CASES)} PageSpec mutations, {len(reg)} registry mutations, {len(gc)} wrapper-gate cases)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
