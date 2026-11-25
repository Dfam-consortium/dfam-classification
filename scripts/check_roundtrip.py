#!/usr/bin/env python3
"""Check that the 1.0.0 conversion lost nothing.

Compares the built TEClasses.tsv, without its id column, against the
original Dfam 4.0 file. Every difference must be one of the encoding or
whitespace fixes listed below. Anything else fails.
"""

import argparse
import os
import sys

import dfc

# (original line number, column) for every cell the conversion was meant
# to change. Line numbers count the header as line 1.
EXPECTED = {
    (3, "title"),              # trailing space
    (23, "description"),       # double-encoded UTF-8
    (27, "title"),             # double-encoded UTF-8
    (57, "wicker_equiv"),      # trailing space
    (58, "wicker_equiv"),      # trailing space
    (172, "description"),      # double-encoded UTF-8
}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--original", default=os.path.join(
        dfc.ROOT, "legacy", "TEClasses-dfam-4.0.tsv"))
    ap.add_argument("--built", default=os.path.join(
        dfc.ROOT, "build", "TEClasses.tsv"))
    args = ap.parse_args()

    _, original = dfc.read_tsv(args.original)
    _, built = dfc.read_tsv(args.built)
    if len(original) != len(built):
        sys.exit(f"row count differs: {len(original)} vs {len(built)}")

    changed, unexpected = set(), []
    for line, (old, new) in enumerate(zip(original, built), start=2):
        for column in dfc.LEGACY_FIELDS:
            if old[column] == new[column]:
                continue
            changed.add((line, column))
            if (line, column) not in EXPECTED:
                unexpected.append(f"line {line} {column}: "
                                  f"{old[column]!r} -> {new[column]!r}")
            else:
                print(f"fixed line {line} {column}: "
                      f"{old[column][-40:]!r} -> {new[column][-40:]!r}")

    for u in unexpected:
        print(f"UNEXPECTED {u}", file=sys.stderr)
    for line, column in sorted(EXPECTED - changed):
        print(f"MISSING fix at line {line} {column}", file=sys.stderr)
    if unexpected or EXPECTED - changed:
        sys.exit("round trip failed")
    print(f"round trip ok: {len(built)} rows, "
          f"{len(changed)} cells changed, all expected")


if __name__ == "__main__":
    main()
