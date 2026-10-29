#!/usr/bin/env python3
"""Build schema/leakage-patterns.json: the GENERATION_MODE_* pattern registry, derived from the REAL clone source.

Usage:
    python3 extraction/build_leakage_patterns.py           # (re)write schema/leakage-patterns.json
    python3 extraction/build_leakage_patterns.py --check   # exit 1 if the committed registry differs from a fresh build

Every source-derived pattern carries file:line evidence found by searching the real file (src/, CLONE_SPEC*.md,
src/data/blogPosts.json). Source copy is stored only as hashed 5-word shingles (sha256, 16 hex) of NFKC-normalised,
zero-width-stripped, quote/dash-folded, lower-cased text, so the registry never republishes the copy itself.
A short `policy` block holds generic health-claim / rating phrasings that are NOT source-derived (labelled as such):
they encode the consumer-app policy (policy/design-policy.json) that health/development claims and ratings are
must-not-fabricate in generation mode.
Needs the sibling source project; without it --check prints a notice and exits 0.
No human has reviewed these patterns; detection is string-based and can be evaded by paraphrase.
"""
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "schema"))
from textnorm import normalize, shingles  # noqa: E402

OUT = os.path.join(ROOT, "schema", "leakage-patterns.json")


def read(rel):
    with open(os.path.join(SRC, rel), encoding="utf-8") as f:
        return f.read().split("\n")


def ev(rel, needle):
    for i, l in enumerate(read(rel), 1):
        if needle in l:
            return {"cite": f"{rel}:{i}", "anchor": needle}
    raise KeyError(f"{needle!r} not found in {rel}")


def build():
    posts = json.load(open(os.path.join(SRC, "src/data/blogPosts.json")))
    P = "src/data/blogPosts.json"

    brand = [
        {"id": "riley", "regex": r"\briley(?:'s|s)?\b", "evidence": [ev("src/components/SiteFooter.jsx", 'alt="Riley"')]},
        {"id": "riley-spaced", "regex": r"\br[\s._*-]{1,2}i[\s._*-]{1,2}l[\s._*-]{1,2}e[\s._*-]{1,2}y\b", "evidence": [ev("src/components/SiteFooter.jsx", 'alt="Riley"')],
         "note": "letter-separated spelling (R.i.l.e.y, R-I-L-E-Y)"},
        {"id": "rileyapp", "regex": r"rileyapp", "evidence": [ev("src/router.jsx", "'rileyapp.com'")]},
        {"id": "riley-plus", "regex": r"riley\s*plus", "evidence": [ev("src/components/pricing/PricingHero.jsx", "name: 'Riley Plus+'")]},
        {"id": "golden-window", "regex": r"\bgolden window\b", "evidence": [ev(P, '"slug": "introducing-golden-window"')], "note": "Riley product feature name"},
        {"id": "riley-together", "regex": r"\briley together\b", "evidence": [ev(P, '"slug": "introducing-riley-together"')]},
        {"id": "promo-code", "regex": r"rileyblog\d*", "evidence": [ev("src/components/article/placeholderContent.js", "RILEYBLOG20")]},
        {"id": "mascot-family-names", "regex": r"\b(softie|uplifter|worrier)\b", "evidence": [ev("src/components/PersonalizationMarquee.jsx", "softie-family.svg")],
         "note": "Riley parenting-style character names (only the distinctive ones; Spark/Guide/Explorer are ordinary words and are not blocked)"},
    ]

    persons = []
    seen = set()

    def person(name, e, kind):
        n = normalize(re.sub(r"^(dr\.?\s+)", "", name.strip(), flags=re.I))
        n = re.sub(r",?\s*m\.?d\.?$", "", n).strip()
        if n and n not in seen:
            seen.add(n)
            persons.append({"name": n, "regex": r"\b" + re.escape(n) + r"(?!\w)", "kind": kind, "evidence": [e]})

    for line in read("src/components/ClinicalBoard.jsx"):
        for m in re.finditer(r"name: '([^']+)'", line):
            person(m.group(1), ev("src/components/ClinicalBoard.jsx", f"name: '{m.group(1)}'"), "clinician")
    for p in posts:
        for k in ("author", "reviewer"):
            if p.get(k):
                person(p[k], ev(P, f'"{k}": "{p[k]}"'), "author" if k == "author" else "medical-reviewer")
    for m in re.finditer(r"name: '([^']+)'", "\n".join(read("src/components/Testimonials.jsx"))):
        att = m.group(1)
        if att.lower().startswith("app store"):
            continue
        e = ev("src/components/Testimonials.jsx", f"name: '{att}'")
        head = att.split(",")[0].strip()
        if len(head) > 2:
            person(head, e, "testimonial-attribution")
        rel = re.search(r"((?:mom|dad) of baby \w)", att, re.I)
        if rel:
            person(rel.group(1), e, "testimonial-attribution")
    for who, needle in [("naina", "chat_module_naina"), ("seb & daughter", "Seb & daughter testimonial")]:
        person(who, ev("src/components/Featurette.jsx", needle), "user-story")

    orgs = []
    for line in read("src/components/Hero.jsx"):
        m = re.search(r"alt: '([^']+) logo'", line)
        if m and len(m.group(1)) > 2 and m.group(1).lower() != "bump":
            nm = normalize(m.group(1))
            orgs.append({"name": nm, "regex": r"\b" + re.escape(nm) + r"\b", "kind": "press", "evidence": [ev("src/components/Hero.jsx", f"alt: '{m.group(1)} logo'")]})
    orgs.append({"name": "techcrunch", "regex": r"\btech\s?crunch\b", "kind": "press", "evidence": [ev("src/components/Hero.jsx", "alt: 'TC logo'")], "note": "tc.png is the TechCrunch mark"})
    orgs.append({"name": "the bump", "regex": r"\bthe bump\b", "kind": "press", "evidence": [ev("src/components/Hero.jsx", "alt: 'Bump logo'")]})
    cols = re.search(r"const COLUMNS = \[(.*)\]", "\n".join(read("src/components/lower/ComparisonTable.jsx"))).group(1)
    for c in re.findall(r"'([^']+)'", cols):
        if c in ("Riley", "Other Tracking Apps", "Podcasts, Books, & Blogs"):
            continue
        nm = normalize(c)
        orgs.append({"name": nm, "regex": r"\b" + re.escape(nm) + r"\b", "kind": "competitor", "evidence": [ev("src/components/lower/ComparisonTable.jsx", f"'{c}'")]})

    claims = []
    for rel, needle, rx in [
        ("src/components/Hero.jsx", "pediatrician-backed", r"pediatrician[\s-]backed"),
        ("src/components/Hero.jsx", "award-winning", r"award[\s-]winning"),
        ("src/components/FaqClouds.jsx", "science-backed", r"science[\s-]backed"),
        ("src/components/HowRileyWorks.jsx", "expert-reviewed", r"expert[\s-]reviewed"),
        ("src/components/ClinicalBoard.jsx", "evidence-based", r"evidence[\s-]based"),
        ("src/components/upper/superpowersData.js", "pediatrician-vetted", r"pediatrician[\s-]vetted"),
        ("src/components/ClinicalBoard.jsx", "Clinical Advisory Board", r"clinical advisory board"),
        ("src/components/AnnouncementBar.jsx", "7-day free trial", r"\b7[\s-]day free trial\b"),
        ("src/components/pricing/PricingHero.jsx", "$9.99", r"\$\s?9\.99"),
        ("src/components/upper/SiteHeader.jsx", "Try For $0", r"try for \$0"),
        ("src/components/article/placeholderContent.js", "20% off", r"\b20% off\b"),
    ]:
        claims.append({"id": re.sub(r"[^a-z0-9]+", "-", needle.lower()).strip("-"), "regex": rx, "evidence": [ev(rel, needle)]})

    domains = []
    for rel in sorted(glob.glob(os.path.join(SRC, "src", "**", "*.js*"), recursive=True)):
        r = os.path.relpath(rel, SRC)
        if r.endswith(".json"):
            continue
        for i, l in enumerate(read(r), 1):
            for m in re.finditer(r"https?://([a-z0-9.-]+)", l):
                host = m.group(1).removeprefix("www.")
                if host in ("w3.org", "example.com") or host in {d["domain"] for d in domains}:
                    continue
                domains.append({"domain": host, "evidence": [{"cite": f"{r}:{i}", "anchor": m.group(1)}]})
    for host, rel, needle in [("cdn.sanity.io", P, "https://cdn.sanity.io/")]:
        domains.append({"domain": host, "evidence": [ev(rel, needle)]})

    embeds = [{"id": m.group(1), "evidence": [ev("src/pages/LegalPage.jsx", m.group(1))]}
              for m in re.finditer(r"'([0-9a-f]{8}-[0-9a-f-]{27})'", "\n".join(read("src/pages/LegalPage.jsx")))]
    embeds.append({"id": "termly", "evidence": [ev("src/pages/LegalPage.jsx", "termly-embed")]})
    asset_ids = []
    for line in read("src/components/Featurette.jsx"):
        for m in re.finditer(r"(?:artboard|stateMachine): '([^']+)'", line):
            asset_ids.append({"id": m.group(1), "evidence": [ev("src/components/Featurette.jsx", f"'{m.group(1)}'")]})

    store = [
        {"id": "app-store", "regex": r"\bapp\s?store\b", "evidence": [ev("src/components/SiteFooter.jsx", 'alt="Download on the App Store"')]},
        {"id": "download-on-the", "regex": r"\bdownload on the\b", "evidence": [ev("src/components/SiteFooter.jsx", 'alt="Download on the App Store"')]},
        {"id": "onelink", "regex": r"onelink", "evidence": [ev("src/components/upper/SiteHeader.jsx", "rileyapp.onelink.me")]},
        {"id": "apple-logo", "regex": r"\bapple (logo|badge)\b", "evidence": [ev("src/components/Hero.jsx", "/assets/icons/apple-logo.svg")]},
    ]
    ratings = [
        {"id": "real-reviews", "regex": r"real reviews,? real families", "evidence": [ev("src/components/Testimonials.jsx", "Real Reviews, Real Families")]},
        {"id": "app-store-review", "regex": r"app store review", "evidence": [ev("src/components/Testimonials.jsx", "name: 'App Store Review'")]},
        {"id": "eleven-of-ten", "regex": r"\b11/10\b", "evidence": [ev("src/components/Testimonials.jsx", "11/10")]},
    ]

    # ---- copy shingles
    texts = []  # (file, line, text)
    lit = re.compile(r"'([^'\n]{12,})'|\"([^\"\n]{12,})\"|`([^`\n]{12,})`|>([^<>{}\n]{12,})<")

    def is_copy(s):
        w = s.split()
        if len(w) < 5 or "${" in s:
            return False
        if any((":" in x and not x.endswith(":")) or "[" in x or "=" in x or "/" in x for x in w):
            return False
        return sum(1 for x in w if "-" in x) / len(w) < 0.4 and sum(1 for x in w if re.fullmatch(r"[A-Za-z’'.,!?]{3,}", x)) >= 3

    seen_txt = set()
    files = sorted(glob.glob(os.path.join(SRC, "src", "components", "**", "*.js*"), recursive=True)) + \
        sorted(glob.glob(os.path.join(SRC, "src", "pages", "*.jsx")))
    for path in files:
        r = os.path.relpath(path, SRC)
        for i, l in enumerate(read(r), 1):
            if l.strip().startswith("//") or l.strip().startswith("{/*"):
                continue
            for m in lit.finditer(l):
                s = next(g for g in m.groups() if g)
                if is_copy(s):
                    texts.append((r, i, s))
        whole = "\n".join(read(r)).replace("{' '}", " ")
        for m in re.finditer(r">([^<>{}]{12,})<", whole):
            s = re.sub(r"\s+", " ", m.group(1)).strip()
            if ("\n" in m.group(1) or "{' '}" in "\n".join(read(r))) and is_copy(s) and (r, s) not in seen_txt:
                seen_txt.add((r, s))
                texts.append((r, whole.count("\n", 0, m.start()) + 1, s))
    for i, l in enumerate(read(P), 1):
        m = re.match(r'\s*"(title|excerpt|crumbTitle|seoTitle|imageAlt|authorTitle|reviewerTitle)": "(.*)",?$', l)
        if m and len(m.group(2).split()) >= 5:
            texts.append((P, i, m.group(2)))
    for spec in ["CLONE_SPEC.md", "CLONE_SPEC_PAGES_MARKETING.md", "CLONE_SPEC_PAGES_BLOG.md"]:
        for i, l in enumerate(read(spec), 1):
            for m in re.finditer(r"[\"“]([^\"“”\n]{20,})[\"”]", l):
                if is_copy(m.group(1)):
                    texts.append((spec, i, m.group(1)))
    hashes = set()
    per_file = {}
    for r, i, s in texts:
        for sh in shingles(s, 5):
            hashes.add(hashlib.sha256(sh.encode()).hexdigest()[:16])
        pf = per_file.setdefault(r, {"file": r, "strings": 0, "firstLine": i, "lastLine": i})
        pf["strings"] += 1
        pf["firstLine"] = min(pf["firstLine"], i)
        pf["lastLine"] = max(pf["lastLine"], i)
    return {
        "$schema": "riley-design-tokens/schema/leakage-patterns",
        "version": "2.0.0",
        "generatedBy": "extraction/build_leakage_patterns.py (re-run with --check by verify_all.py when the source project is present)",
        "humanReviewed": False,
        "caveat": "No human has reviewed these patterns. Matching is string-based on normalised text: paraphrase, translation or images of text evade it. Treat a pass as 'no known source string found', not as proof of originality.",
        "normalization": "NFKC; zero-width and soft-hyphen characters removed; common Cyrillic/Greek homoglyphs folded to Latin; curly quotes -> straight; all dash variants -> '-'; lower-case; whitespace collapsed (schema/textnorm.py).",
        "brand": brand,
        "persons": persons,
        "organizations": orgs,
        "claims": claims,
        "domains": domains,
        "embedIds": embeds,
        "assetIdentifiers": asset_ids,
        "storeMarks": store,
        "ratings": ratings,
        "policy": {
            "sourceDerived": False,
            "note": "Generic phrasings encoded from policy/design-policy.json (consumer parenting app: health/development claims and ratings are must-not-fabricate in generation mode). Not found in the source; pinned by policy.",
            "claims": [r"clinically (proven|tested|validated)", r"medically (proven|approved)", r"(pediatrician|doctor|physician)[\s-](approved|recommended|endorsed|backed|vetted)",
                       r"\bfda[\s-](approved|cleared)\b", r"\b(prevents?|reduces? (the )?risk of) sids\b", r"\bcures?\b", r"\bguaranteed (to|results?|sleep)\b",
                       r"\bdiagnos(e|es|is|ing)\b", r"\b\d+% of (parents|families|babies|users)\b", r"\b(trusted|loved|used) by [\d,.]+\s*k?\+?\s*(parents|families|users)\b"],
            "ratings": [r"[★☆⭐]", r"\b[0-5](\.\d)?\s*(/\s*5|out of 5|stars?)\b", r"\b\d[\d,.]*\s*k?\+?\s*(reviews|ratings)\b", r"\brated\s+\d", r"(^|\s)#1\b"],
        },
        "copyShingles": {"n": 5, "hash": "sha256 hex[:16] of the space-joined normalised 5-word window (punctuation stripped)",
                         "sources": sorted(per_file.values(), key=lambda x: x["file"]), "count": len(hashes), "hashes": sorted(hashes)},
    }


def main(argv):
    if not os.path.isdir(os.path.join(SRC, "src")):
        print("source project absent: leakage patterns not rebuilt")
        return 0
    reg = build()
    if "--check" in argv:
        cur = json.load(open(OUT))
        if cur != reg:
            diff = [k for k in reg if cur.get(k) != reg[k]]
            print(f"DRIFT: schema/leakage-patterns.json differs from a fresh build in {diff}")
            return 1
        print("leakage patterns up to date")
        return 0
    with open(OUT, "w") as f:
        json.dump(reg, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(reg['persons'])} persons, {len(reg['organizations'])} orgs, {reg['copyShingles']['count']} shingles")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
