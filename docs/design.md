# Dfam classification as a versioned ontology

Design proposal. Draft of 2026-09-15, revised 2026-10-02.
Baseline data: `TEClasses.tsv` from Dfam 4.0, 299 terms.

## 1. Summary

The Dfam classification is a curated tree of repeat classes. Dfam currently identifies each term by its full path from the root, so any
rename or move changes the identity of every descendant, and curators have
no way to say that a term in one release is the same term in the next.

The tree stays as it is. The design adds three things:

1. A permanent, opaque identifier for every term.
2. Explicit rules for retiring, merging and splitting terms, so family
   assignments can be remapped mechanically.
3. A versioned release process with a machine-readable diff and a
   path-to-ID table for every release.

The full path and the RepeatMasker type/subtype remain the two display
forms. The identifier is the join key underneath them and is not meant to
be shown to users by default.

We convert the 4.0 tree unchanged as version 1.0.0 and make the planned
classification update as version 2.0.0, so the update is the first revision
that exercises the obsoletion and remapping rules.

## 2. The current file

`TEClasses.tsv` has one row per term and eleven columns: the full path,
title, description, hyperlink, family count, RepeatMasker type and subtype,
and equivalents in Repbase, Wicker, Curcio-Derbyshire and Piegu.

| Fact | Value |
|---|---|
| Terms | 299 |
| Top-level roots | 7 |
| Maximum depth | 11 |
| Grouping terms with no RepeatMasker label | 63 |
| Terms with a RepeatMasker label but zero families | 19 |
| Local names reused under different parents | 14 |
| Families in `Interspersed_Repeat;Unknown` | 5,143,116 of 7,627,663 |

Properties of the tree that the design preserves:

- It is a decision key. Curators apply one criterion at each level, and
  the order in which they apply the criteria is itself curated information. Some edges
  are mechanism, some are transposase or reverse-transcriptase phylogeny,
  some are viral taxonomy, some are structure, and some are genomic
  location.
- Every term has exactly one parent.
- The RepeatMasker type/subtype pair is unique per term, and grouping
  terms have none.
- The full path is always shown, so local names such as `L2-end` and
  `Deu-core` may legitimately recur under different parents.

The tree is not an OWL class hierarchy in the logical sense. An edge means
"this is the next split in the key", not "every instance of the child is
an instance of the parent" in a way a reasoner should extend. Exports to
OBO or OWL exist for tooling and interoperability, and the build declares
the hierarchy as asserted only.

## 3. Identifiers

Every term gets a permanent numeric identifier in CURIE form, for example
`DFC:0000123`.

- Zero-padded, seven digits, assigned from a counter that only increases.
- Never reused, even after a term is retired.
- Means the same thing for good. A label, definition wording or parent
  can change under the same ID, but the group of elements it names
  should only grow. Section 8 gives the rule and its one exception.
- Carries no meaning. Position in the tree, rank and name live in the
  term record, not in the ID.
- Check the prefix against Bioregistry for collisions, then register it,
  so that IDs resolve at a Dfam URL such as
  `https://dfam.org/classification/DFC:0000123`.

The 1.0.0 baseline assigns IDs in the row order of the 4.0 file, which
makes the first assignment deterministic and easy to review.

## 4. Term record

| Field | Meaning | Required |
|---|---|---|
| `id` | Permanent identifier | yes |
| `label` | Local name, the last path segment | yes |
| `parent` | ID of the parent term, empty for roots | yes |
| `title` | One-line description, from the current `title` column | for assignable terms |
| `definition` | Longer description, from the current `description` column | no |
| `definition_source` | PMIDs, DOIs or URLs supporting the definition | no |
| `criterion` | Basis for this split: mechanism, phylogeny, structure, host taxon, location | recommended |
| `assignable` | Whether families may be assigned to this term | yes |
| `placeholder` | True for `Unknown` and `Other`, so tools can treat them as unclassified | yes |
| `rm_type`, `rm_subtype` | RepeatMasker label, unique per term | for assignable terms |
| `status` | `active` or `obsolete` | yes |
| `replaced_by` | Single successor for a retired term | for merges |
| `consider` | Candidate successors for a retired term | for splits |
| `created_in` | Classification version that introduced the term | yes |
| `obsoleted_in` | Classification version that retired the term | for obsolete terms |
| `last_path` | Full path frozen at the time of retirement | for obsolete terms |
| `comment` | Free text for curators | no |

Derived at build time, not stored in the source:

- Full path from root, built from labels along the parent chain.
- Depth.
- Family count. A count belongs to a Dfam release, so it lives in a
  per-release statistics file.

## 5. Source files and build

The source of truth is a small set of TSV files in a git repository.
They stay editable in a spreadsheet, which is how curators maintain the
classification today, and they diff cleanly.

| File | Contents |
|---|---|
| `terms.tsv` | One row per term, the fields in section 4 |
| `mappings.sssom.tsv` | External equivalents, one row per mapping, SSSOM format |
| `synonyms.tsv` | Other names for a term, with an OBO scope: exact, broad, narrow or related |
| `last-id` | Highest ID number ever issued |
| `VERSION` | Classification version being prepared |
| `CHANGELOG.md` | Human-readable notes per release |

A build script produces the release artifacts:

- `dfam-classification.obo` and `.owl`, for ontology tooling and for
  loading into OLS or BioPortal.
- `dfam-classification.json` in OBO Graphs form, for web use.
- `TEClasses.tsv` in the current eleven-column shape, for existing
  tools, with an added `id` column.
- `paths.tsv`, mapping every path that has ever existed to its ID, with
  the first and last classification versions in which the path named
  that term, and the term's path in the current version.
- `diff.tsv`, listing terms added, retired, relabeled, reparented and
  remapped since the previous version.

Validation runs on every pull request and before every release:

- IDs unique and never reused.
- Exactly one parent per term, no cycles, no orphans.
- Labels unique among siblings.
- RepeatMasker labels unique across active terms, absent on
  non-assignable terms.
- Every obsolete term has `obsoleted_in`, `last_path`, and either
  `replaced_by` or `consider`.
- `replaced_by` points at an active term, so chains do not form.
- Every mapping subject is a known ID.
- No non-ASCII mojibake, no leading or trailing whitespace.
- Every assignable term has a title. The validator only warns about
  this for now, because 149 of the 236 assignable terms in Dfam 4.0 have
  none.

## 6. External mappings

The Repbase, Wicker, Curcio-Derbyshire and Piegu columns become rows in
`mappings.sssom.tsv`. Each row has a subject ID, a predicate, an object
label, the source system, a confidence, and a comment.

| Current column value | SSSOM row |
|---|---|
| `D/T (TIR)/A (hAT)` on every hAT child | One row on the `hAT` term with `skos:broadMatch`; children inherit |
| `R/L (LTR)/R (Retrovirus) ??` | Object `R/L (LTR)/R (Retrovirus)`, confidence low, comment "curator marked ??" |
| `non-LTR/RTE (and 1 RTETP)` | Object `non-LTR/RTE`, comment "one family is RTETP" |
| `non-LTR/-` | No row |

Clade-level systems such as Wicker are asserted once at the most general
term where they hold. Term-level systems such as Repbase are asserted
per term. Tools that need a mapping for a term walk up the tree until
they find one.

In 1.0.0 we keep every legacy value as written, one `skos:closeMatch`
row per non-empty cell, so the conversion stays lossless. Collapsing
values onto the clade term and turning flags such as `??` into a
confidence and comment change content, so we will do both in a later
version.

RepeatMasker type/subtype is Dfam's own operational label, so it stays a
property of the term record instead of a mapping row.

Curators can add cross-references to the Sequence Ontology for the upper
tiers and to NCBI Taxonomy for viral taxa such as Retroviridae in the
same file when convenient.

## 7. Versioning

The classification has its own semantic version, independent of the
Dfam release number. Each Dfam release states which classification
version it was built with.

| Change | Bump |
|---|---|
| Definition wording, typo, mapping confidence, encoding fix | Patch |
| New term, new synonym, new mapping | Minor |
| Relabel or reparent an existing term | Minor. IDs and family assignments stay valid; paths change |
| Retire, merge or split a term | Major |
| Change an existing RepeatMasker label | Major |

An ID needs no version next to it, because its meaning does not change.
As far as we know GO works the same way: its annotation files carry GO
IDs with no version, and a reader resolves an old ID against the current
release. Exports should write the ID on each entry. A file may also record, once in its header, the
classification version it was built with, which helps in debugging but
which no reader needs.

A path is different. A rename leaves the old path naming nothing, and
when a retired term's label is reused (section 8) the same path names a
different term. A file that carries a path without an ID, which means
everything Dfam published up to 4.0, needs the version it came from
whenever its path is ambiguous.

Curators never delete a term. A retired term keeps its record, its last
path and its RepeatMasker label, so old annotation output stays
interpretable.

## 8. Retiring terms and remapping families

### Keep the ID or retire it

The test for any change: would a family that was correctly assigned to
this ID before the change be wrong after it? If not, the term keeps its
ID. If so, curators retire the ID.

| What happened | ID | Kind of change | Example |
|---|---|---|---|
| Some families were on the wrong term, but no term's meaning changed | Keep | None. Curators move the families; the classification gets no release | A family filed under Tip100 belongs under hAT5 |
| Definition reworded, boundary unchanged | Keep | Patch | Charlie's description gains a citation |
| A new group is added under the term | Keep | Minor | Activator gains a child, Activator-X. Families on Activator stay correct, and curators can move some of them down |
| The term is renamed, or moved to a new parent, and still names the same elements | Keep | Minor | Tip100 becomes Tip100-like |
| The term absorbs another term | Keep the survivor. Retire the absorbed term with `replaced_by` | Major | hAT6 merges into hAT5. Every hAT5 family is still correct |
| Part of what the term named moves to a new sibling, outside it | Retire with `consider` | Major | Charlie splits into Charlie-A and Charlie-B |
| A small boundary correction moves a few families to a sibling | Curators' judgment. Usually keep, and list the moved families in the changelog | Patch | Three hAT5 families turn out to be hAT6 |

Moving a term's own families is curation either way, and curators
review the same families whether the ID survives or not. Retiring
matters to people outside Dfam who hold the ID in a paper, in old
RepeatMasker output or in another database, because Dfam cannot
reassign their copies. Suppose a 2026 paper lists elements as
DFC:0000089, and Charlie later narrows. If Charlie had kept the ID, a
reader in 2030 would resolve DFC:0000089 to the narrower Charlie, which
is wrong for any element that now belongs in Charlie-B, and nothing
would warn them. With the ID retired, the lookup says that Charlie was
split and names both candidates.

A retired term's label may pass to a new term. After a split, curators
may well want the core group to keep the familiar name, so a new
DFC:0000303 labelled Charlie replaces the retired DFC:0000089. The
path `…;hAT;Charlie` then names DFC:0000089 up to 1.1.0 and DFC:0000303
from 2.0.0. `paths.tsv` and the `classification_path` table record that
range. A lookup by path should take the version the path came from. If the
version is unknown and the path is ambiguous, the lookup should flag it
for a curator and not guess.

### Forms of retirement

Retirement takes one of three forms.

| Case | Term record | Fix for assigned families |
|---|---|---|
| Merge, or retirement with one successor | `replaced_by: DFC:x` | Automatic |
| Split | `consider: DFC:x, DFC:y` | Curator decides per family |
| Retirement with no successor | Neither | Curator decides. Validation forbids this for terms that have families |

One query finds stale assignments:

```sql
SELECT f.accession, f.classification_id, c.replaced_by_id
FROM family f
JOIN classification c ON c.id = f.classification_id
WHERE c.status = 'obsolete';
```

Run it when a new classification version is loaded and as a scheduled
check. Refuse at insert time to assign an obsolete ID.

The automatic case is one update:

```sql
UPDATE family f
JOIN classification c ON c.id = f.classification_id
SET f.classification_id = c.replaced_by_id
WHERE c.status = 'obsolete' AND c.replaced_by_id IS NOT NULL;
```

Validation requires `replaced_by` to name an active term, so one step
always reaches an active term. When a later release retires that
successor, curators update the older term's `replaced_by` as well.

For a split, the changelog entry lists how many families sit on the
retired term, so curators know the worklist size before release.
Where the split follows something already on the family record, such as
host taxon, a rule can bulk-assign and curators check the remainder.

Order of operations at release time:

1. Load the new classification version.
2. Apply the automatic remap.
3. Generate and work the split worklist.
4. Regenerate the cached path and RepeatMasker columns.

Step 4 comes last so that the site never displays a family with the path
of a retired term.

## 9. Changes to the Dfam database and exports

`schema-changes.md` lists the column-level changes. In outline:

- The numeric part of the DFC identifier becomes `classification.id`,
  so the existing foreign keys from `family` and `coding_sequence` stay.
  Loading 1.0.0 renumbers the 4.0 ids once.
- `classification` gains `status`, `assignable`, `placeholder`,
  `replaced_by_id`, `created_in` and `obsoleted_in`. For a retired term,
  `lineage` holds its last path, so there is no separate `last_path`
  column.
- New tables hold split candidates (`classification_consider`), every
  path ever used (`classification_path`) and the loaded releases
  (`classification_version`). `db_version` records which classification
  version a Dfam release uses.
- `family` gets no version column. After each load every family points
  at an active term of the current classification version.
- The database keeps a `root` row with id 0, which the ontology lacks.

Exports change little:

- HMM and EMBL files can carry the ID and the classification version
  next to the existing path line.
- famdb carries the term table for the version it was built with, so
  clients can resolve IDs offline.
- The website shows the path or the RepeatMasker label as now, and
  resolves the ID URL to the term page.

## 10. Migration plan

We convert the 4.0 tree unchanged first, then make the planned
classification update as a separate revision.

Version 1.0.0, the baseline:

1. Assign IDs to all 299 terms in file order.
2. Split the file into `terms.tsv` and `mappings.sssom.tsv`. Move the
   count column to a Dfam 4.0 statistics file.
3. Fix only non-semantic defects: the three rows with UTF-8 mojibake and
   the three fields with trailing whitespace.
4. Regenerate the legacy `TEClasses.tsv` from the new source and diff it
   against the original. The diff must be empty apart from the encoding
   and whitespace fixes.
5. Run validation, tag 1.0.0, and load it into the database. The load
   renumbers the 4.0 ids to DFC numbers once, as `schema-changes.md`
   describes.

Version 2.0.0, the update:

1. Make the classification changes in `terms.tsv`, retiring terms with
   `replaced_by` or `consider` rather than editing them in place.
2. Resolve the semantic questions listed in section 11 and record each
   decision in the changelog.
3. Run validation and build. Review `diff.tsv` and the split worklist
   sizes.
4. Tag 2.0.0 and follow the release order in section 8.

With the two steps separate, we can prove the 1.0.0 conversion lossless
by diffing, and the 2.0.0 changelog lists only classification decisions.
If a family lands somewhere unexpected, one step or the other caused it.

Version 1.0.0 does not need a public Dfam release. The next Dfam release
states that it uses classification 2.0.0.

## 11. Defects and open questions in the 4.0 file

Non-semantic, fix in 1.0.0:

- Lines 23, 27 and 172 contain double-encoded UTF-8, for example
  `CACTAâ¦TAGTG` for `CACTA…TAGTG` and `Â±` for `±`. Line 23 needs a
  second fix. Its ellipsis appears to have been typed as Mac Roman byte
  0xC9, so undoing the double encoding gives `TAGÉCTA`. The conversion
  script maps that to `TAG…CTA`.
- Trailing whitespace in the title of `Normally_Non-integrating_Virus`
  and in the Wicker value `D/T (TIR)/P ` on two rows.

Semantic, decide in 2.0.0:

- `Retroviridae` has RepeatMasker subtype `Cassandra` and 254 families.
  Cassandra is a plant TRIM-related element, so this looks like a row
  misalignment.
- `Viper-group;TATE` has RepeatMasker type `Unknown` while its sibling
  `Viper` is `LTR`.
- `ERV1;SINE-like` has RepeatMasker type `SINE` under an LTR node.
- `Helicase;Helitron-1` has RepeatMasker subtype `Helitron`, not
  `Helitron-1`.
- Wicker values `DNA/` on `Kolobok-H` and `non-LTR/` on several LINE
  terms look incomplete. They may mean "no subclass" or may be truncated.
- 19 terms have a RepeatMasker label but no families. Decide whether to
  keep them.

## 12. Governance

- Public git repository holding the source files, build script and
  validation: https://github.com/Dfam-consortium/dfam-classification.
- Issue template for term requests: label, parent, title, evidence,
  proposed RepeatMasker label.
- Pull requests run validation. A release is a git tag plus the built
  artifacts, changelog, diff and path-to-ID table.
- Curators edit `terms.tsv` directly. No ontology editor is required.

## Appendix: example records

A term row in `terms.tsv`:

```
id            DFC:0000217
label         L2-end
parent        DFC:0000214
title         SINE with a tRNA promoter, Deu core and L2-derived 3' end.
criterion     structure
assignable    true
placeholder   false
rm_type       SINE
rm_subtype    tRNA-Deu-L2
status        active
created_in    1.0.0
```

Its derived path:

```
Interspersed_Repeat;Transposable_Element;Class_I_Retrotransposition;LINE-dependent_Retroposon;SINE;tRNA_Promoter;Deu-core;L2-end
```

A mapping row in `mappings.sssom.tsv`:

```
subject_id    DFC:0000217
predicate_id  skos:closeMatch
object_label  SINE/SINE2
object_source Repbase
confidence    1.0
comment
```

A retired term after a merge in 2.0.0:

```
id            DFC:0000031
label         Chapaev-3
status        obsolete
obsoleted_in  2.0.0
replaced_by   DFC:0000030
last_path     Interspersed_Repeat;Transposable_Element;Class_II_DNA_Transposition;Transposase;CACTA;CMC;Chapaev_group;Chapaev-3
```
