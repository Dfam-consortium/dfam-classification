"""Shared helpers for reading and writing the classification source files."""

import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TERMS = os.path.join(ROOT, "terms.tsv")
MAPPINGS = os.path.join(ROOT, "mappings.sssom.tsv")
SYNONYMS = os.path.join(ROOT, "synonyms.tsv")
LAST_ID = os.path.join(ROOT, "last-id")
VERSION = os.path.join(ROOT, "VERSION")

PREFIX = "DFC"
ID_RE = re.compile(r"^DFC:\d{7}$")

TERM_FIELDS = [
    "id", "label", "parent", "title", "definition", "hyperlink", "criterion",
    "assignable", "placeholder", "rm_type", "rm_subtype", "status",
    "replaced_by", "consider", "created_in", "obsoleted_in", "last_path",
    "comment",
]

MAPPING_FIELDS = [
    "subject_id", "subject_label", "predicate_id", "object_label",
    "object_source", "mapping_justification", "comment",
]

SYNONYM_FIELDS = ["id", "synonym", "scope", "comment"]

# OBO synonym scopes. "related" is the least specific.
SYNONYM_SCOPES = {"exact", "broad", "narrow", "related"}

# The four freeform equivalence columns of the legacy TEClasses.tsv,
# keyed by the object_source value used in mappings.sssom.tsv.
LEGACY_EQUIV = {
    "Repbase": "repbase_equiv",
    "Wicker": "wicker_equiv",
    "Curcio-Derbyshire": "curcio_derbyshire_equiv",
    "Piegu": "piegu_equiv",
}

LEGACY_FIELDS = [
    "full_name", "title", "description", "hyperlink", "count",
    "repeatmasker_type", "repeatmasker_subtype", "repbase_equiv",
    "wicker_equiv", "curcio_derbyshire_equiv", "piegu_equiv",
]

SSSOM_HEADER = """\
#curie_map:
#  DFC: https://dfam.org/classification/DFC:
#  skos: http://www.w3.org/2004/02/skos/core#
#  semapv: https://w3id.org/semapv/vocab/
#mapping_set_id: https://dfam.org/classification/mappings.sssom.tsv
#license: https://creativecommons.org/publicdomain/zero/1.0/
"""


def format_id(n):
    return f"{PREFIX}:{n:07d}"


def id_number(term_id):
    return int(term_id.split(":", 1)[1])


def read_tsv(path):
    """Read a TSV with a header row, skipping '#' metadata lines."""
    with open(path, encoding="utf-8", newline="") as fh:
        lines = [line for line in fh if not line.startswith("#")]
    reader = csv.DictReader(lines, delimiter="\t",
                            quoting=csv.QUOTE_NONE, quotechar=None)
    return reader.fieldnames, list(reader)


def write_tsv(path, fields, rows, header=""):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(header)
        writer = csv.DictWriter(fh, fields, delimiter="\t",
                                quoting=csv.QUOTE_NONE, quotechar=None,
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_terms(path=TERMS):
    return read_tsv(path)[1]


def write_terms(rows, path=TERMS):
    write_tsv(path, TERM_FIELDS, rows)


def read_mappings(path=MAPPINGS):
    return read_tsv(path)[1]


def write_mappings(rows, path=MAPPINGS):
    write_tsv(path, MAPPING_FIELDS, rows, header=SSSOM_HEADER)


def read_synonyms(path=SYNONYMS):
    return read_tsv(path)[1]


def write_synonyms(rows, path=SYNONYMS):
    write_tsv(path, SYNONYM_FIELDS, rows)


def read_version():
    with open(VERSION, encoding="utf-8") as fh:
        return fh.read().strip()


def paths_by_id(terms):
    """Full root-to-term path for every term that has an ID."""
    by_id = {t["id"]: t for t in terms if t["id"]}
    paths = {}

    def path(term_id, seen=()):
        if term_id in paths:
            return paths[term_id]
        if term_id in seen:
            raise ValueError(f"cycle through {term_id}")
        term = by_id[term_id]
        parent = term["parent"]
        prefix = path(parent, seen + (term_id,)) + ";" if parent else ""
        paths[term_id] = prefix + term["label"]
        return paths[term_id]

    for term_id in by_id:
        path(term_id)
    return paths


def tree_order(terms):
    """Active terms in depth-first order, siblings in terms.tsv row order."""
    children = {}
    for t in terms:
        if t["status"] == "active":
            children.setdefault(t["parent"], []).append(t)
    ordered = []

    def visit(parent):
        for t in children.get(parent, []):
            ordered.append(t)
            visit(t["id"])

    visit("")
    return ordered
