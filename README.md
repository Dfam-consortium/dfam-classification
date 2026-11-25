# Dfam classification

The Dfam classification of repeat families, kept as a versioned ontology.
Each term has a permanent identifier such as `DFC:0000123`. The full path
from the root and the RepeatMasker type/subtype remain the labels people
see. `docs/design.md` explains the reasoning behind the layout.

The repository is https://github.com/Dfam-consortium/dfam-classification.
Releases, with the built files attached, are on its releases page.

## Files

| File | Contents |
|---|---|
| `terms.tsv` | One row per term. This is the file curators edit. |
| `mappings.sssom.tsv` | Equivalent classes in Repbase, Wicker, Curcio-Derbyshire and Piegu |
| `synonyms.tsv` | Other names a term goes by, such as Wicker's three-letter codes |
| `last-id` | Highest ID number ever issued |
| `VERSION` | Version being prepared |
| `CHANGELOG.md` | What changed in each version |
| `stats/` | Family counts per Dfam release |
| `releases/` | The built files of each release |
| `legacy/` | The Dfam 4.0 files that version 1.0.0 was converted from |
| `scripts/` | Validation, ID assignment and build |

## Editing

1. Edit `terms.tsv` in a spreadsheet or text editor, keeping it
   tab-separated UTF-8.
2. For a new term, add a row with the `id` column empty and run
   `make ids`. That fills in the next free ID, plus `status` and
   `created_in` where they are empty. If the new term needs a child,
   assign the parent's ID before adding the child.
3. Never delete a row. To retire a term, set `status` to `obsolete`, fill
   `obsoleted_in` and `last_path`, and point `replaced_by` at its single
   successor or list candidates in `consider`.
4. Run `make` to validate and build. `python3 scripts/validate.py -v` also
   lists warnings.

`CONTRIBUTING.md` describes how a change gets from a proposal to a
release.

## Building

`make` writes to `build/`:

- `TEClasses.tsv`, the familiar eleven-column layout with an `id` column
  added in front.
- `paths.tsv`, mapping each known path to its ID and current path.

`make roundtrip` checks that the 1.0.0 build reproduces the Dfam 4.0 file,
apart from six encoding and whitespace fixes. Once terms change, the
check no longer applies.

The scripts use only the Python standard library. We have run them with
Python 3.12 only.

## Versions

The classification has its own version number, separate from Dfam
releases. Version 1.0.0 is the Dfam 4.0 classification with only
encoding and whitespace fixes. See `docs/design.md` for when to bump
each part of the version.

## License

The classification, the mappings and the scripts are released under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/); see
`LICENSE`.
