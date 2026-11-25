# Dfam schema changes for the versioned classification

Proposal for the `schema-work` branch of Internal-Use-Schemata, 2026-10-02.
It applies the design in `design.md` to the Dfam MySQL schema. Every
change below is a change to the MySQL Workbench model unless it says
otherwise.

## The main decision

The numeric part of the permanent ID becomes `classification.id`.
`DFC:0000123` is the row with `id = 123`. The foreign keys in `family`,
`coding_sequence` and `classification_has_wikipedia` keep working as they
do now. Only their values change, once, when we load classification 1.0.0.

Before choosing this we searched Dfam-API, Dfam-Portal, Server, Lib,
FamDB and RepeatMasker for uses of the id. Outside the database it turned
up in two places: the API's `coding_seqs[].classification_id` field and
the DfamCache pickle. The HMM, EMBL, Stockholm and FASTA exports, FamDB
and RepeatMasker write the lineage path or the RepeatMasker Type/SubType
and no id. The search did not read `Server/reportCompletion.py` or
`Server/export_dfam.py` closely, so check those two before the renumber.

The database keeps one row the ontology does not have: `root`, with
`id = 0`. The API tree and every `lineage` string start from it. The
loader creates that row. It has no DFC term.

The loader never deletes a row. A retired term keeps its row with
`status = 'obsolete'`, so old family records and old IDs always resolve.

## `classification`

| Column | Change | Comment text for the model |
|---|---|---|
| `id` | Remove AUTO_INCREMENT | Numeric part of the permanent DFC identifier: 123 is DFC:0000123. 0 is the database-only root. Never reused. |
| `name` | None | The term's label, the last segment of its path. |
| `parent_id` | Add FK `fk_classification_parent` to `classification.id` | Parent term. 0 for the seven top-level terms, NULL for root. |
| `tooltip` | Comment only | One-line title of the term, from `title` in terms.tsv. |
| `description` | None | |
| `hyperlink` | None | |
| `repeatmasker_type_id`, `repeatmasker_subtype_id` | None | |
| `sort_order` | Comment only | Position among siblings, from row order in terms.tsv. Set by the loader. |
| `repbase_equiv`, `wicker_equiv`, `curcio_derbyshire_equiv`, `piegu_equiv` | Comment only | Closest equivalent in the named system, from mappings.sssom.tsv. Set by the loader. |
| `lineage` | Comment only | Semicolon-separated path from root to this term. Set by the loader. For an obsolete term, the path it had when it was retired. |
| `aliases` | Comment only | Comma-separated other names for the term, from synonyms.tsv. Set by the loader. |
| `status` | New. `ENUM('active','obsolete') NOT NULL DEFAULT 'active'` | Obsolete terms stay in the table so that old IDs resolve. |
| `assignable` | New. `TINYINT(1) NOT NULL DEFAULT 0` | 1 if families may be assigned to this term. |
| `placeholder` | New. `TINYINT(1) NOT NULL DEFAULT 0` | 1 for Unknown and Other, which mean "not classified further". |
| `replaced_by_id` | New. `BIGINT NULL`, FK `fk_classification_replaced_by` to `classification.id` | For an obsolete term with one successor, the active term that replaced it. |
| `created_in` | New. `VARCHAR(16) NOT NULL` | Classification version that introduced the term. |
| `obsoleted_in` | New. `VARCHAR(16) NULL` | Classification version that retired the term. |

New table comment: "The Dfam repeat classification, loaded from a
versioned release of the dfam-classification repository. A tree through
parent_id. Edit the repository, not this table."

The current comment calls it a nested set, which it isn't.

## New tables

### `classification_consider`

Candidate successors for a term that was split. A retired term has
either `replaced_by_id` or rows here, never both.

| Column | Type | Comment |
|---|---|---|
| `classification_id` | `BIGINT NOT NULL`, PK, FK to `classification.id` | The retired term. |
| `candidate_id` | `BIGINT NOT NULL`, PK, FK to `classification.id` | An active term that families on the retired term may move to. |

### `classification_path`

Every path any release has used, with the versions in which it named
each term. It replaces the `DEPRECATED_CLASSES` dictionary hard-coded in
`Lib/DfamValidations.py`.

| Column | Type | Comment |
|---|---|---|
| `path` | `VARCHAR(512) NOT NULL`, PK | A full path without the `root;` prefix. The longest today is 174 characters. |
| `first_version` | `VARCHAR(16) NOT NULL`, PK, FK to `classification_version.version` | First classification version in which this path named this term. |
| `last_version` | `VARCHAR(16) NULL`, FK to `classification_version.version` | Last version in which it did. NULL while the path is current. |
| `classification_id` | `BIGINT NOT NULL`, FK to `classification.id`, indexed | The term this path named in that range. |

The same path can appear in several rows when a retired term's label
passes to a new term. To resolve a path from a file, pick the row whose
range contains the file's classification version. Compare versions
through `classification_version.release_date`, since version strings do
not sort correctly as text. If the file's version is unknown and the
path has more than one row, report it to a curator instead of picking
one.

### `classification_version`

One row for each classification release loaded into this database.

| Column | Type | Comment |
|---|---|---|
| `version` | `VARCHAR(16) NOT NULL`, PK | Such as 1.0.0. |
| `release_date` | `DATE NOT NULL` | Date of the release tag. |
| `git_commit` | `VARCHAR(40) NULL` | Commit the release was built from. |
| `loaded_date` | `DATETIME NOT NULL` | When it was loaded here. |

## Changes to other tables

- `db_version`: add `classification_version VARCHAR(16) NULL`, FK to
  `classification_version.version`. Each Dfam release records the
  classification it uses here.
- `coding_sequence`: add FK `fk_coding_sequence_classification1` from
  `classification_id` to `classification.id`. The column has no FK today.
- `repeatmasker_type`, `repeatmasker_subtype`: delete "This is deprecated"
  from the table comments. Type/SubType is the public label of a term.
- `family`: add a trigger that rejects a retired term.

```sql
CREATE TRIGGER family_classification_bi BEFORE INSERT ON family
FOR EACH ROW
BEGIN
  IF NEW.classification_id IS NOT NULL AND EXISTS (
       SELECT 1 FROM classification
       WHERE id = NEW.classification_id AND status = 'obsolete') THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'classification term is obsolete';
  END IF;
END;

CREATE TRIGGER family_classification_bu BEFORE UPDATE ON family
FOR EACH ROW
BEGIN
  IF NOT (NEW.classification_id <=> OLD.classification_id)
     AND EXISTS (
       SELECT 1 FROM classification
       WHERE id = NEW.classification_id AND status = 'obsolete') THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'classification term is obsolete';
  END IF;
END;
```

Retiring a term does not fire these triggers. They fire only when a
family row is written, so they stop new assignments to retired terms and
leave the release remap free to move families off them.

## Unchanged on purpose

- `classification_has_wikipedia` and `wikipedia` stay as they are.
- The four `*_equiv` columns stay as the database form of the mappings.
  Each holds one value per term, which fits all of today's data. A fifth
  system, or a term needing two values from one system, would need a
  `classification_mapping` table.
- `family` gets no classification version column. IDs are stable and
  retired rows stay, so after each release load every family points at
  an active term of the version named in `db_version`.

## What the release loader does

The loader is a script outside the model, and nobody has written it yet.
For each classification release it will:

1. Insert or update every term by `id`, including the root row, and
   delete nothing.
2. Fill `classification_consider`, `classification_path` and the
   denormalized columns: `lineage`, `sort_order`, `aliases` and the four
   `*_equiv` columns.
3. Insert the `classification_version` row.
4. Move families off merged terms:

   ```sql
   UPDATE family f
   JOIN classification c ON c.id = f.classification_id
   SET f.classification_id = c.replaced_by_id
   WHERE c.status = 'obsolete' AND c.replaced_by_id IS NOT NULL;
   ```

5. List the families on split terms for curators:

   ```sql
   SELECT f.accession, c.id AS retired_id,
          GROUP_CONCAT(k.candidate_id) AS candidates
   FROM family f
   JOIN classification c ON c.id = f.classification_id
   JOIN classification_consider k ON k.classification_id = c.id
   WHERE c.status = 'obsolete'
   GROUP BY f.accession, c.id;
   ```

6. Once that list is empty, set `db_version.classification_version`.

The repository's validator requires `replaced_by` to name an active
term. When a later release retires that successor too, curators update
the older term's `replaced_by` in the same change. One step from any
retired term therefore always reaches an active term.

## Loading 1.0.0 into the 4.0 database

This happens once.

1. Build a map from old id to new id by joining `classification.lineage`
   to the 1.0.0 `paths.tsv` with `root;` added. All 299 terms must
   match, and root maps to 0. Commit the map to the repository for
   `Server/compareDBs.py` and other comparisons against releases older
   than 1.0.0.
2. In one transaction, with `FOREIGN_KEY_CHECKS = 0`, rewrite
   `classification.id` and `parent_id`, `family.classification_id`,
   `coding_sequence.classification_id` and
   `classification_has_wikipedia.classification_id`. Old and new ids
   overlap, so first add an offset such as 1,000,000 to every old id,
   then map from the offset values.
3. Apply the model changes above, then run the loader for 1.0.0.
4. Check that no `family.classification_id` points at a missing or
   obsolete term.
5. Rebuild the DfamCache pickle with `Server/buildDfamCache.py`. A stale
   cache would make bulk import write old ids.

## Code to update outside the schema

- Dfam-API, `utils/family.js:283`: return `coding_seqs[].classification_id`
  as the string `DFC:0000123`, and update the examples in
  `api/openapi.yaml`.
- Dfam-API, `services/ClassificationService.js`: select only
  `status = 'active'` rows. Add `sort_order` to the SELECT on line 17.
  Line 82 sorts by it, but the query never fetches it, so children come
  back in name order.
- `Lib/DfamValidations.py`: look old paths up in `classification_path`
  instead of `DEPRECATED_CLASSES`.
- `Server/updateClassificationLineage.py`: retire it, since the loader
  now sets `lineage`.
- `Server/compareDBs.py`: compare releases from 1.0.0 onward by id, and
  older ones through the map from step 1.
