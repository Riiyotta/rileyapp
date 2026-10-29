#!/usr/bin/env python3
"""Whole-page-wrapper quality gate (R9). Called by verify_all.py; also runnable alone.

    python3 extraction/wrapper_gate.py

Input: extraction/measured-values.json `sectionHeights` (measured on the BUILT clone at 1440px with
extraction/measure_sections.mjs) and extraction/wrapper-whitelist.json.
Rules (thresholds pinned HERE in code, not read from JSON):
  * HERO section taller than 1800px -> warn; taller than 3000px -> error unless whitelisted.
  * one in-flow section holding > 50% of its page height -> warn; > 60% -> error unless whitelisted.
    Pages with fewer than 3 in-flow non-SHELL sections are skipped; SHELL sections (announcement, header,
    footer) are excluded; fixed/sticky overlays take no page height and are never measured.
  * every template must have a measurement and every required node of the template a measured height -> else error.
  * measurement at any viewport other than 1440 -> error.
  * whitelist entries need reviewedBy, a justification of 30+ chars and maxHeightPx above the measured height;
    stale (no matching measurement) or over-cap entries fail; an agent reviewer must say
    "agent attestation, not a human sign-off". A whitelisted hit still warns.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEWPORT = 1440
HERO_WARN_PX = 1800
HERO_ERROR_PX = 3000
SHARE_WARN = 0.50
SHARE_ERROR = 0.60
MIN_INFLOW_SECTIONS = 3
AGENT_ATTESTATION = "agent attestation, not a human sign-off"


def J(rel):
    with open(os.path.join(ROOT, rel)) as f:
        return json.load(f)


def sections_meta():
    out = {}
    d = os.path.join(ROOT, "sections")
    for fn in os.listdir(d):
        if fn.endswith(".json"):
            c = json.load(open(os.path.join(d, fn)))
            out[c["id"]] = c
    return out


def run(measured=None, whitelist=None, templates=None, sections=None):
    measured = measured if measured is not None else J("extraction/measured-values.json")
    whitelist = whitelist if whitelist is not None else J("extraction/wrapper-whitelist.json")
    templates = templates if templates is not None else J("templates/templates.json")
    sections = sections if sections is not None else sections_meta()
    errors, warns = [], []
    sh = measured.get("sectionHeights")
    if not isinstance(sh, dict):
        return ["sectionHeights missing from extraction/measured-values.json"], warns
    if sh.get("viewport") != VIEWPORT:
        errors.append(f"sectionHeights measured at viewport {sh.get('viewport')}, gate requires {VIEWPORT}")
    pages = sh.get("templates", {})
    wl = {(e.get("template"), e.get("section")): e for e in whitelist.get("entries", [])}
    used_wl = set()
    for e in whitelist.get("entries", []):
        rb = e.get("reviewedBy", "")
        if not rb:
            errors.append(f"whitelist {e.get('template')}/{e.get('section')}: reviewedBy missing")
        elif "agent" in rb.lower() and AGENT_ATTESTATION not in rb:
            errors.append(f"whitelist {e.get('template')}/{e.get('section')}: agent reviewer must state '{AGENT_ATTESTATION}'")
        if len(e.get("justification", "")) < 30:
            errors.append(f"whitelist {e.get('template')}/{e.get('section')}: justification must be 30+ characters")
    for tname, t in templates["templates"].items():
        if tname not in pages:
            errors.append(f"template {tname}: no sectionHeights measurement")
            continue
        m = pages[tname]
        measured_ids = [s["section"] for s in m["sections"]]
        for n in t["nodes"]:
            if n["required"] and n["section"] not in measured_ids:
                errors.append(f"template {tname}: required node {n['section']} has no measured height")
        for s in m["sections"]:
            if s.get("height") is None:
                errors.append(f"template {tname}: {s['section']} measurement is missing (null)")
        page_h = m.get("pageHeight") or 0
        inflow = [s for s in m["sections"] if s.get("height") is not None
                  and sections.get(s["section"], {}).get("semantic", {}).get("category") != "SHELL"
                  and sections.get(s["section"], {}).get("placement") != "global-overlay"]
        for s in m["sections"]:
            if s.get("height") is None:
                continue
            cat = sections.get(s["section"], {}).get("semantic", {}).get("category")
            key = (tname, s["section"])
            entry = wl.get(key)
            if cat == "HERO" and s["height"] > HERO_WARN_PX:
                if s["height"] > HERO_ERROR_PX and not entry:
                    errors.append(f"{tname}/{s['section']}: HERO {s['height']}px > {HERO_ERROR_PX}px")
                else:
                    warns.append(f"{tname}/{s['section']}: HERO {s['height']}px > {HERO_WARN_PX}px" + (" (whitelisted)" if entry else ""))
                if entry:
                    used_wl.add(key)
            if len(inflow) >= MIN_INFLOW_SECTIONS and s in inflow and page_h:
                share = s["height"] / page_h
                if share > SHARE_WARN:
                    if share > SHARE_ERROR and not entry:
                        errors.append(f"{tname}/{s['section']}: holds {share:.0%} of the page (> {SHARE_ERROR:.0%})")
                    else:
                        warns.append(f"{tname}/{s['section']}: holds {share:.0%} of the page (> {SHARE_WARN:.0%})" + (" (whitelisted)" if entry else ""))
                    if entry:
                        used_wl.add(key)
            if entry and s["height"] > entry.get("maxHeightPx", 0):
                errors.append(f"whitelist {tname}/{s['section']}: measured {s['height']}px exceeds maxHeightPx {entry.get('maxHeightPx')}")
    for key in set(wl) - used_wl:
        errors.append(f"whitelist {key[0]}/{key[1]}: stale entry (no gate hit in the current measurements)")
    return errors, warns


def main():
    errors, warns = run()
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"wrapper gate: {len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
