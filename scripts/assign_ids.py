#!/usr/bin/env python3
"""Give every term in terms.tsv that has an empty id the next free ID.

The last-id file holds the highest number ever issued. IDs are never
reused, so a number stays spent even if its row is later dropped before
release. New terms also get created_in from VERSION and status active
when those cells are empty.
"""

import argparse

import dfc


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="show what would be assigned without writing")
    args = ap.parse_args()

    terms = dfc.read_terms()
    with open(dfc.LAST_ID, encoding="utf-8") as fh:
        last = int(fh.read().strip())
    version = dfc.read_version()

    assigned = []
    for t in terms:
        if t["id"]:
            continue
        last += 1
        t["id"] = dfc.format_id(last)
        t["status"] = t["status"] or "active"
        t["created_in"] = t["created_in"] or version
        assigned.append(t)
        print(f"{t['id']}\t{t['label']}")

    if not assigned:
        print("no terms without an id")
        return
    if args.dry_run:
        return
    dfc.write_terms(terms)
    with open(dfc.LAST_ID, "w", encoding="utf-8") as fh:
        fh.write(f"{last}\n")


if __name__ == "__main__":
    main()
