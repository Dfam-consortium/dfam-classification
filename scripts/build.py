#!/usr/bin/env python3
"""Build release artifacts from terms.tsv and mappings.sssom.tsv.

Writes to the output directory:
  TEClasses.tsv  the legacy eleven-column layout with an id column first.
                 Counts come from --counts and are blank without it.
  paths.tsv      every path any release has used, the first and last
                 versions in which it named a term, that term's ID,
                 its current path and status. last_version is empty
                 while the path is current. Earlier history comes from
                 --previous-paths, the paths.tsv of the last release.
"""

import argparse
import os

import dfc


def legacy_rows(terms, mappings, counts):
    paths = dfc.paths_by_id(terms)
    equiv = {}
    for m in mappings:
        column = dfc.LEGACY_EQUIV.get(m["object_source"])
        if column:
            equiv.setdefault(m["subject_id"], {})[column] = m["object_label"]
    for t in dfc.tree_order(terms):
        row = {
            "id": t["id"],
            "full_name": paths[t["id"]],
            "title": t["title"],
            "description": t["definition"],
            "hyperlink": t["hyperlink"],
            "count": counts.get(t["id"], ""),
            "repeatmasker_type": t["rm_type"],
            "repeatmasker_subtype": t["rm_subtype"],
        }
        for column in dfc.LEGACY_EQUIV.values():
            row[column] = equiv.get(t["id"], {}).get(column, "")
        yield row


PATH_FIELDS = ["path", "first_version", "last_version", "id",
               "current_path", "status"]


def path_rows(terms, previous, version, previous_version):
    """Carry the previous release's path history forward one version.

    A path that still names the same term keeps its row. A row that no
    longer holds is closed at previous_version. A path new in this
    version, including a reused label, gets a row starting at version.
    """
    current = dfc.paths_by_id(terms)
    status = {t["id"]: t["status"] for t in terms}
    live = {(current[t["id"]], t["id"])
            for t in terms if t["status"] == "active"}
    rows = []
    for p in previous:
        row = dict(p)
        if not row["last_version"]:
            if (row["path"], row["id"]) in live:
                live.discard((row["path"], row["id"]))
            else:
                row["last_version"] = previous_version
        rows.append(row)
    for path, term_id in live:
        rows.append({"path": path, "first_version": version,
                     "last_version": "", "id": term_id})
    for row in rows:
        active = status.get(row["id"]) == "active"
        row["current_path"] = current[row["id"]] if active else ""
        row["status"] = status.get(row["id"], "unknown")
    rows.sort(key=lambda r: (r["path"], dfc.id_number(r["id"])))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=os.path.join(dfc.ROOT, "build"))
    ap.add_argument("--counts", help="per-release family counts TSV")
    ap.add_argument("--previous-paths", help="paths.tsv from the last release")
    ap.add_argument("--previous-version",
                    help="version of the last release; needed with "
                    "--previous-paths")
    args = ap.parse_args()
    if bool(args.previous_paths) != bool(args.previous_version):
        ap.error("--previous-paths and --previous-version go together")

    terms = dfc.read_terms()
    mappings = dfc.read_mappings()
    counts = {}
    if args.counts:
        counts = {r["id"]: r["count"] for r in dfc.read_tsv(args.counts)[1]}
    previous = []
    if args.previous_paths:
        previous = dfc.read_tsv(args.previous_paths)[1]

    os.makedirs(args.out, exist_ok=True)
    dfc.write_tsv(os.path.join(args.out, "TEClasses.tsv"),
                  ["id"] + dfc.LEGACY_FIELDS,
                  legacy_rows(terms, mappings, counts))
    dfc.write_tsv(os.path.join(args.out, "paths.tsv"), PATH_FIELDS,
                  path_rows(terms, previous, dfc.read_version(),
                            args.previous_version))
    print(f"wrote {args.out}/TEClasses.tsv and {args.out}/paths.tsv "
          f"for version {dfc.read_version()}")


if __name__ == "__main__":
    main()
