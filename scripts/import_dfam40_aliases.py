#!/usr/bin/env python3
"""One-time import of the Dfam 4.0 classification aliases into synonyms.tsv.

TEClasses.tsv did not carry the aliases column, so this reads a snapshot
of https://dfam.org/api/classes taken from the Dfam 4.0 release. Every
alias becomes a synonym with scope "related", which claims nothing about
how close the meaning is. Curators can narrow the scope later.

Kept for the record. Do not rerun it once anyone has edited synonyms.tsv.
"""

import argparse
import json
import os
import sys

import dfc


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--snapshot", default=os.path.join(
        dfc.ROOT, "legacy", "dfam-4.0-api-classes.json"))
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing synonyms.tsv")
    args = ap.parse_args()

    if os.path.exists(dfc.SYNONYMS) and not args.force:
        sys.exit("synonyms.tsv already exists; use --force to overwrite")

    with open(args.snapshot, encoding="utf-8") as fh:
        tree = json.load(fh)
    paths = dfc.paths_by_id(dfc.read_terms())
    id_of_path = {path: term_id for term_id, path in paths.items()}

    aliases = {}

    def walk(node):
        path = node["full_name"].removeprefix("root;")
        if node.get("aliases"):
            aliases[path] = node["aliases"]
        for child in node.get("children") or []:
            walk(child)

    walk(tree)

    rows = []
    for path, value in aliases.items():
        if path not in id_of_path:
            sys.exit(f"alias on unknown path {path}")
        for alias in value.split(","):
            if alias.strip():
                rows.append({"id": id_of_path[path], "synonym": alias.strip(),
                             "scope": "related", "comment": ""})
    rows.sort(key=lambda r: dfc.id_number(r["id"]))
    dfc.write_synonyms(rows)
    print(f"{len(rows)} synonyms on {len(aliases)} terms")


if __name__ == "__main__":
    main()
