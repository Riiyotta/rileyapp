#!/usr/bin/env python3
"""Build tokens/llm/token-catalog.json from the real token files (R10). Self-contained (no source project needed).

Usage:
    python3 extraction/build_token_catalog.py           # rewrite the catalog
    python3 extraction/build_token_catalog.py --check   # exit 1 if the committed catalog differs from the token files

Every leaf token (an object carrying `value` or `ref`) under tokens/<layer>/*.json becomes one catalog entry keyed by
its canonical path `tokens.<layer>.<file>.<key...>`, with its category and resolved value. Nothing is hand-typed, so
the catalog cannot drift from the token files without --check (run by verify_all.py) failing.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tokens", "llm", "token-catalog.json")
LAYERS = ["00-foundation", "10-semantic", "20-component", "30-layout"]
# file -> catalog category (special-cased sub-groups below)
CATEGORY = {
    "color": "color", "gradient": "gradient", "radius": "radius", "elevation": "elevation", "breakpoint": "breakpoint",
    "motion": "motion", "color-roles": "color-roles", "typography-roles": "typography-roles", "motion-roles": "motion-roles",
    "button": "button", "card": "card", "nav": "nav", "pill": "pill", "table": "table",
    "container": "container", "section-spacing": "section-spacing",
}


def leaves(o, path):
    if isinstance(o, dict):
        if "value" in o or "ref" in o:
            yield path, o
            return
        for k, v in o.items():
            if k in ("evidence", "$schema") or k.endswith("Evidence"):
                continue
            yield from leaves(v, path + [k])


def build():
    tokens = {}
    for layer in LAYERS:
        for p in sorted(glob.glob(os.path.join(ROOT, "tokens", layer, "*.json"))):
            name = os.path.splitext(os.path.basename(p))[0]
            doc = json.load(open(p))
            for path, leaf in leaves(doc, []):
                cat = CATEGORY.get(name, name)
                if name == "typography":
                    cat = "font-family" if path[0] == "families" else "type-scale"
                key = ".".join(["tokens", layer, name] + path)
                val = leaf.get("value", leaf.get("ref"))
                tokens[key] = {"category": cat, "value": val if isinstance(val, (str, int, float)) else json.dumps(val, ensure_ascii=False)}
    themes = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "tokens", "themes", "*.json"))):
        t = json.load(open(p))
        themes[t["id"]] = sorted(t["colorRoles"])
    cats = sorted({v["category"] for v in tokens.values()})
    return {
        "$schema": "riley-design-tokens/llm/token-catalog",
        "generatedBy": "extraction/build_token_catalog.py (verify_all.py re-runs it with --check)",
        "note": "Every token a generator may reference, by canonical path. PageSpec node.style values must be one of these keys (schema/semantic_validate.py TOKEN_* rules). Prefer 20-component > 10-semantic > 00-foundation.",
        "categories": {c: sorted({".".join(k.split(".")[:3]) for k, v in tokens.items() if v["category"] == c}) for c in cats},
        "themes": themes,
        "fontFamilies": sorted(k for k, v in tokens.items() if v["category"] == "font-family"),
        "counts": {c: sum(1 for v in tokens.values() if v["category"] == c) for c in cats},
        "tokens": dict(sorted(tokens.items())),
    }


def main(argv):
    cat = build()
    if "--check" in argv:
        cur = json.load(open(OUT))
        if cur != cat:
            print("DRIFT: tokens/llm/token-catalog.json differs from the token files")
            return 1
        print("token catalog up to date")
        return 0
    with open(OUT, "w") as f:
        json.dump(cat, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote token catalog: {len(cat['tokens'])} tokens in {len(cat['categories'])} categories")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
