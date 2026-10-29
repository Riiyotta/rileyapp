#!/usr/bin/env python3
"""Draft-07 structural check of every schema/examples/*.pagespec.json (and the section-contract schema).

Usage: python3 schema/validate_schema.py [pagespec.json ...]
Checks the schema itself (check_schema) and prints every Draft7Validator error.
Semantic rules (template sequence, maxWords, routes, asset policy) live in
schema/semantic_validate.py. Root derived from __file__.
"""
import glob
import json
import os
import sys

from jsonschema import Draft7Validator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv):
    with open(os.path.join(ROOT, "schema/pagespec.schema.json")) as f:
        schema = json.load(f)
    Draft7Validator.check_schema(schema)
    v = Draft7Validator(schema)
    bad = 0
    with open(os.path.join(ROOT, "schema/section-contract.schema.json")) as f:
        Draft7Validator.check_schema(json.load(f))
    for p in argv or sorted(glob.glob(os.path.join(ROOT, "schema/examples/*.pagespec.json"))):
        with open(p) as f:
            errs = list(v.iter_errors(json.load(f)))
        print(f"Draft7Validator {os.path.basename(p)}: {len(errs)} error(s)")
        for e in errs:
            print("  ", list(e.absolute_path), e.message[:200])
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
