#!/usr/bin/env python3
"""One-time conversion of the Dfam 4.0 TEClasses.tsv to classification 1.0.0.

Writes terms.tsv, mappings.sssom.tsv, last-id and the Dfam 4.0 family
counts. Apart from layout, it changes content in two ways: it repairs
double-encoded UTF-8, including one Mac Roman ellipsis, and strips
leading and trailing whitespace. check_roundtrip.py confirms this by
comparing a rebuild against the original file.

Kept for the record. Do not rerun it once anyone has edited terms.tsv.
"""

import argparse
import os
import sys

import dfc

PLACEHOLDERS = {"Interspersed_Repeat;Unknown", "Other"}

# The Academ description's ellipsis looks like Mac Roman byte 0xC9 that
# something read as Latin-1 "\u00c9" before the double encoding.
MAC_ROMAN_FIXES = {"TAG\u00c9CTA": "TAG\u2026CTA"}


def fix_text(value):
    """Undo double-encoded UTF-8 and strip surrounding whitespace."""
    if any(ord(c) > 127 for c in value):
        try:
            value = value.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    for wrong, right in MAC_ROMAN_FIXES.items():
        value = value.replace(wrong, right)
    return value.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--legacy", default=os.path.join(
        dfc.ROOT, "legacy", "TEClasses-dfam-4.0.tsv"))
    ap.add_argument("--counts", default=os.path.join(
        dfc.ROOT, "stats", "dfam-4.0-family-counts.tsv"))
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing terms.tsv")
    args = ap.parse_args()

    if os.path.exists(dfc.TERMS) and not args.force:
        sys.exit("terms.tsv already exists; use --force to overwrite")

    version = dfc.read_version()
    fields, legacy = dfc.read_tsv(args.legacy)
    if fields != dfc.LEGACY_FIELDS:
        sys.exit(f"unexpected columns in {args.legacy}: {fields}")

    terms, mappings, counts = [], [], []
    id_of_path = {}
    for n, row in enumerate(legacy, start=1):
        row = {k: fix_text(v) for k, v in row.items()}
        path = row["full_name"]
        parent_path, _, label = path.rpartition(";")
        term_id = dfc.format_id(n)
        id_of_path[path] = term_id
        has_rm_label = bool(row["repeatmasker_type"]
                            or row["repeatmasker_subtype"])
        terms.append({
            "id": term_id,
            "label": label,
            "parent": id_of_path[parent_path] if parent_path else "",
            "title": row["title"],
            "definition": row["description"],
            "hyperlink": row["hyperlink"],
            "criterion": "",
            "assignable": "true" if has_rm_label else "false",
            "placeholder": "true" if path in PLACEHOLDERS else "false",
            "rm_type": row["repeatmasker_type"],
            "rm_subtype": row["repeatmasker_subtype"],
            "status": "active",
            "replaced_by": "",
            "consider": "",
            "created_in": version,
            "obsoleted_in": "",
            "last_path": "",
            "comment": "",
        })
        for source, column in dfc.LEGACY_EQUIV.items():
            if row[column]:
                mappings.append({
                    "subject_id": term_id,
                    "subject_label": label,
                    "predicate_id": "skos:closeMatch",
                    "object_label": row[column],
                    "object_source": source,
                    "mapping_justification": "semapv:ManualMappingCuration",
                    "comment": "",
                })
        if row["count"]:
            counts.append({"id": term_id, "path": path, "count": row["count"]})

    dfc.write_terms(terms)
    dfc.write_mappings(mappings)
    dfc.write_tsv(args.counts, ["id", "path", "count"], counts)
    with open(dfc.LAST_ID, "w", encoding="utf-8") as fh:
        fh.write(f"{len(terms)}\n")
    print(f"{len(terms)} terms, {len(mappings)} mappings, "
          f"{len(counts)} counts")


if __name__ == "__main__":
    main()
