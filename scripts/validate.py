#!/usr/bin/env python3
"""Check the classification source files against the classification rules.

With --previous, also check that no term from an earlier release has
disappeared. Exits non-zero if any check fails.
"""

import argparse
import re
import sys

import dfc

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
# A UTF-8 lead byte read as Latin-1 followed by a continuation byte, a
# common sign of text encoded twice.
MOJIBAKE_RE = re.compile("[Â-ô][\u0080-¿]")
BOOLEANS = {"true", "false"}


class Checker:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, message):
        self.errors.append(f"{where}: {message}")

    def warn(self, where, message):
        self.warnings.append(f"{where}: {message}")


def check_text(chk, where, row):
    for field, value in row.items():
        if value is None:
            chk.error(where, "row has too few columns")
            return
        if value != value.strip():
            chk.error(where, f"{field} has leading or trailing whitespace")
        if MOJIBAKE_RE.search(value):
            chk.error(where, f"{field} looks double-encoded: {value!r}")


def check_terms(chk, fields, terms, last_id):
    if fields != dfc.TERM_FIELDS:
        chk.error("terms.tsv", f"columns must be {dfc.TERM_FIELDS}")
        return

    by_id = {}
    for n, t in enumerate(terms, start=2):
        where = f"terms.tsv line {n}"
        check_text(chk, where, t)
        term_id = t["id"]
        if not term_id:
            chk.error(where, f"{t['label']} has no id; run assign_ids.py")
            continue
        if not dfc.ID_RE.match(term_id):
            chk.error(where, f"malformed id {term_id!r}")
            continue
        if term_id in by_id:
            chk.error(where, f"duplicate id {term_id}")
        elif dfc.id_number(term_id) > last_id:
            chk.error(where, f"{term_id} is above last-id {last_id}")
        by_id[term_id] = t

    siblings, rm_labels = {}, {}
    for term_id, t in by_id.items():
        where = term_id
        active = t["status"] == "active"
        if t["status"] not in ("active", "obsolete"):
            chk.error(where, "status must be active or obsolete")
        if not t["label"] or ";" in t["label"]:
            chk.error(where, f"bad label {t['label']!r}")
        for field in ("assignable", "placeholder"):
            if t[field] not in BOOLEANS:
                chk.error(where, f"{field} must be true or false")
        if not SEMVER_RE.match(t["created_in"]):
            chk.error(where, "created_in must be a version such as 1.0.0")

        parent = t["parent"]
        if parent and parent not in by_id:
            chk.error(where, f"parent {parent} does not exist")
        elif active and parent and by_id[parent]["status"] != "active":
            chk.error(where, f"parent {parent} is obsolete")

        rm = (t["rm_type"], t["rm_subtype"])
        if t["assignable"] == "true":
            if not t["rm_type"]:
                chk.error(where, "assignable term has no rm_type")
            # 149 of the 236 assignable Dfam 4.0 terms lack a title. Make
            # this an error once curators have filled them in.
            if not t["title"]:
                chk.warn(where, "assignable term has no title")
        elif any(rm):
            chk.error(where, "non-assignable term has a RepeatMasker label")

        retirement = ("replaced_by", "consider", "obsoleted_in", "last_path")
        if active:
            for field in retirement:
                if t[field]:
                    chk.error(where, f"active term has {field}")
            key = (parent, t["label"])
            if key in siblings:
                chk.error(where, f"label {t['label']} repeats under the "
                          f"same parent as {siblings[key]}")
            siblings[key] = term_id
            if any(rm):
                if rm in rm_labels:
                    chk.error(where, f"RepeatMasker label {'/'.join(rm)} "
                              f"also used by {rm_labels[rm]}")
                rm_labels[rm] = term_id
        else:
            if not SEMVER_RE.match(t["obsoleted_in"]):
                chk.error(where, "obsolete term needs obsoleted_in")
            if not t["last_path"]:
                chk.error(where, "obsolete term needs last_path")
            if not (t["replaced_by"] or t["consider"]):
                chk.error(where, "obsolete term needs replaced_by or consider")
            if t["replaced_by"] and t["consider"]:
                chk.error(where, "use replaced_by or consider, not both")
            successors = [t["replaced_by"]] if t["replaced_by"] else []
            successors += [c.strip() for c in t["consider"].split(",")
                           if c.strip()]
            for s in successors:
                if s not in by_id or by_id[s]["status"] != "active":
                    chk.error(where, f"successor {s} is not an active term")

    try:
        dfc.paths_by_id(list(by_id.values()))
    except (ValueError, KeyError) as e:
        chk.error("terms.tsv", f"cannot build paths: {e}")
    return by_id


def check_mappings(chk, fields, mappings, by_id):
    if fields != dfc.MAPPING_FIELDS:
        chk.error("mappings.sssom.tsv", f"columns must be {dfc.MAPPING_FIELDS}")
        return
    for n, m in enumerate(mappings, start=1):
        where = f"mapping {n}"
        check_text(chk, where, m)
        term = by_id.get(m["subject_id"])
        if term is None:
            chk.error(where, f"unknown subject_id {m['subject_id']}")
        elif m["subject_label"] != term["label"]:
            chk.error(where, f"subject_label {m['subject_label']!r} does not "
                      f"match {term['label']!r}")
        for field in ("predicate_id", "object_label", "object_source",
                      "mapping_justification"):
            if not m[field]:
                chk.error(where, f"{field} is empty")


def check_synonyms(chk, fields, synonyms, by_id):
    if fields != dfc.SYNONYM_FIELDS:
        chk.error("synonyms.tsv", f"columns must be {dfc.SYNONYM_FIELDS}")
        return
    seen = set()
    for n, s in enumerate(synonyms, start=2):
        where = f"synonyms.tsv line {n}"
        check_text(chk, where, s)
        if s["id"] not in by_id:
            chk.error(where, f"unknown id {s['id']}")
        # The database stores synonyms comma-separated in
        # classification.aliases.
        if not s["synonym"] or "," in s["synonym"]:
            chk.error(where, f"bad synonym {s['synonym']!r}")
        if s["scope"] not in dfc.SYNONYM_SCOPES:
            chk.error(where, "scope must be one of "
                      f"{sorted(dfc.SYNONYM_SCOPES)}")
        key = (s["id"], s["synonym"])
        if key in seen:
            chk.error(where, f"duplicate synonym {s['synonym']!r}")
        seen.add(key)


def check_previous(chk, previous, by_id):
    for t in previous:
        if not t["id"]:
            continue
        if t["id"] not in by_id:
            chk.error(t["id"], "was in the previous release and is now gone; "
                      "retire it instead of deleting it")
        elif by_id[t["id"]]["created_in"] != t["created_in"]:
            chk.error(t["id"], "created_in changed since the previous release")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--previous", help="terms.tsv from the previous release")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="list warnings as well as errors")
    args = ap.parse_args()

    chk = Checker()
    with open(dfc.LAST_ID, encoding="utf-8") as fh:
        last_id = int(fh.read().strip())
    if not SEMVER_RE.match(dfc.read_version()):
        chk.error("VERSION", "must be a version such as 1.0.0")
    fields, terms = dfc.read_tsv(dfc.TERMS)
    by_id = check_terms(chk, fields, terms, last_id) or {}
    fields, mappings = dfc.read_tsv(dfc.MAPPINGS)
    check_mappings(chk, fields, mappings, by_id)
    fields, synonyms = dfc.read_tsv(dfc.SYNONYMS)
    check_synonyms(chk, fields, synonyms, by_id)
    if args.previous:
        check_previous(chk, dfc.read_tsv(args.previous)[1], by_id)

    if args.verbose:
        for w in chk.warnings:
            print(f"warning: {w}", file=sys.stderr)
    for e in chk.errors:
        print(e, file=sys.stderr)
    if chk.errors:
        sys.exit(f"{len(chk.errors)} problem(s)")
    print(f"ok: {len(terms)} terms, {len(mappings)} mappings, "
          f"{len(synonyms)} synonyms, "
          f"{len(chk.warnings)} warning(s)")


if __name__ == "__main__":
    main()
