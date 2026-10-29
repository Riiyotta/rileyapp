#!/usr/bin/env python3
"""Derive each section contract's closed `source` provenance object from its implementedBy citation (R7).

Usage:
    python3 extraction/build_provenance.py           # rewrite `source` in every sections/*.json
    python3 extraction/build_provenance.py --check   # exit 1 if any contract's `source` differs from a fresh derivation

source = {id, tag, file, lines}: `file` and the range end come from implementedBy[0]; `lines` starts at the FIRST
line inside that range that opens a lowercase (DOM) element, and `tag` is that element's name. `source.id` is
"src:<file stem>@<start line>" so it can never equal the AI-facing `semantic.id` (= contract id).
`semantic` {id, category} is taxonomy and is NOT derived here (it is authored in the contract and checked by
verify_all.py against the closed SEMANTIC_CATEGORIES set).
Needs the sibling source project (design-repo's parent); without it --check prints a notice and exits 0.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.dirname(ROOT)
TAG_RX = re.compile(r"<([a-z][a-z0-9]*)\b")
CITE_RX = re.compile(r"^(?P<path>[^:]+):(?P<a>\d+)(?:-(?P<b>\d+))?$")


def derive(contract):
    m = CITE_RX.match(contract["implementedBy"][0]["cite"])
    path, a = m["path"], int(m["a"])
    b = int(m["b"]) if m["b"] else a
    with open(os.path.join(SRC, path), encoding="utf-8") as f:
        lines = f.read().split("\n")
    for i in range(a, len(lines) + 1):
        hit = TAG_RX.search(lines[i - 1])
        if hit:
            end = max(b, i)
            stem = os.path.splitext(os.path.basename(path))[0]
            return {"id": f"src:{stem}@{i}", "tag": hit.group(1), "file": path, "lines": f"{i}-{end}"}
    raise ValueError(f"{contract['id']}: no DOM element opens at/after {path}:{a}")


def main(argv):
    check = "--check" in argv
    if not os.path.isdir(os.path.join(SRC, "src")):
        print("source project absent: provenance not re-derived")
        return 0
    bad = 0
    for p in sorted(glob.glob(os.path.join(ROOT, "sections", "*.json"))):
        with open(p) as f:
            d = json.load(f)
        src = derive(d)
        if check:
            if d.get("source") != src:
                print(f"DRIFT {d['id']}: source {d.get('source')} != derived {src}")
                bad += 1
            continue
        out = {}
        for k, v in d.items():
            if k == "source":
                continue
            out[k] = v
            if k == "implementedBy":
                out["source"] = src
        with open(p, "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
            f.write("\n")
    print(f"provenance {'checked' if check else 'written'}: {bad} drift")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
