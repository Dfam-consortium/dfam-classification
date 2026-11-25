# Changelog

## 1.0.0

The Dfam 4.0 classification in the new layout. We added, removed,
renamed and moved no terms.

- Assigned DFC:0000001 to DFC:0000299 in the row order of the Dfam 4.0
  `TEClasses.tsv`.
- Split the file into `terms.tsv` and `mappings.sssom.tsv`, and moved
  family counts to `stats/dfam-4.0-family-counts.tsv`.
- Marked the 236 terms with a RepeatMasker label as assignable, and
  `Interspersed_Repeat;Unknown` and `Other` as placeholders.
- Kept each Repbase, Wicker, Curcio-Derbyshire and Piegu value as
  written, as one `skos:closeMatch` mapping per value.
- Copied the 46 aliases on 36 terms into `synonyms.tsv` with scope
  `related`. `TEClasses.tsv` lacks the aliases, so they came from a
  snapshot of the Dfam 4.0 `/api/classes` response.
- Repaired double-encoded UTF-8 in three rows: the Academ description,
  the CACTA title and the SINE description.
- Removed trailing spaces from the `Normally_Non-integrating_Virus` title
  and from two Wicker values.
