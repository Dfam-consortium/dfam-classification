# Changelog

## 2.0.0

The reconciled Repbase and Dfam classification. Generated from the
curators' change list; paths below leave off the leading
`Interspersed_Repeat;Transposable_Element;` where it applies.

### Added

The new terms have no title or definition yet.

- DFC:0000300 `Interspersed_Repeat;Multicopy_RNA_Gene`, RNA
- DFC:0000301 `Interspersed_Repeat;Multicopy_RNA_Gene;snoRNA`, snoRNA
- DFC:0000302 `Class_II_DNA_Transposition;HUH_Transposase;Replitron`, DNA/Replitron
- DFC:0000303 `Class_II_DNA_Transposition;HUH_Transposase;Rolling_Circle`, DNA/RC-Helitron
- DFC:0000304 `Class_II_DNA_Transposition;DDE_Transposase;IS481EU`, DNA/IS481EU
- DFC:0000305 `Class_I_Retrotransposition;LINE;Group-3`, no RepeatMasker label
- DFC:0000306 `Class_I_Retrotransposition;Retrotransposon;HEART`, HEART
- DFC:0000307 `Class_II_DNA_Transposition;DDE_Transposase;PIF-Harbinger;ISL2EU-group`, no RepeatMasker label
- DFC:0000308 `Class_I_Retrotransposition;Retrotransposon;Long_Terminal_Repeat_Element;Troyka`, LTR/Troyka
- DFC:0000309 `Class_II_DNA_Transposition;DDE_Transposase;CMCT;CMC;Plavaka`, DNA/CMC-Plavaka
- DFC:0000310 `Class_I_Retrotransposition;Retrotransposon;Long_Terminal_Repeat_Element;Gypsy-ERV;Retroviridae;Lo-group`, no RepeatMasker label
- DFC:0000311 `Class_I_Retrotransposition;Retrotransposon;Long_Terminal_Repeat_Element;Gypsy-ERV;Retroviridae;Lo-group;Lodin`, LTR/Lodin
- DFC:0000312 `Class_I_Retrotransposition;Retrotransposon;Long_Terminal_Repeat_Element;Gypsy-ERV;Retroviridae;Lo-group;Lokiretrovirus`, LTR/Loki

### Moved

The IDs stay. A path reflects any rename as well.

- DFC:0000007 rRNA: `Interspersed_Repeat;Pseudogene;RNA;rRNA` to `Interspersed_Repeat;Multicopy_RNA_Gene;rRNA`
- DFC:0000008 scRNA: `Interspersed_Repeat;Pseudogene;RNA;scRNA` to `Interspersed_Repeat;Multicopy_RNA_Gene;scRNA`
- DFC:0000009 snRNA: `Interspersed_Repeat;Pseudogene;RNA;snRNA` to `Interspersed_Repeat;Multicopy_RNA_Gene;snRNA`
- DFC:0000010 tRNA: `Interspersed_Repeat;Pseudogene;RNA;tRNA` to `Interspersed_Repeat;Multicopy_RNA_Gene;tRNA`
- DFC:0000116 Ambal: `Class_I_Retrotransposition;LINE;Group-I;Ambal` to `Class_I_Retrotransposition;LINE;Ambal`
- DFC:0000117 CRE: `Class_I_Retrotransposition;LINE;Group-I;CRE` to `Class_I_Retrotransposition;LINE;CRE`
- DFC:0000120 Odin: `Class_I_Retrotransposition;LINE;Group-I;Odin` to `Class_I_Retrotransposition;LINE;Odin`
- DFC:0000123 Group-1: `Class_I_Retrotransposition;LINE;Group-II;Group-1` to `Class_I_Retrotransposition;LINE;Group-1`
- DFC:0000130 Proto-1: `Class_I_Retrotransposition;LINE;Group-II;Group-1;Proto-1` to `Class_I_Retrotransposition;LINE;Proto-1`
- DFC:0000132 Hero: `Class_I_Retrotransposition;LINE;Group-II;Group-1;R2-like;Hero` to `Class_I_Retrotransposition;LINE;Hero`
- DFC:0000139 Group-2: `Class_I_Retrotransposition;LINE;Group-II;Group-2` to `Class_I_Retrotransposition;LINE;Group-2`
- DFC:0000140 Proto-2: `Class_I_Retrotransposition;LINE;Group-II;Group-2;Proto-2` to `Class_I_Retrotransposition;LINE;Proto-2`
- DFC:0000019 Helitron-1: `Class_II_DNA_Transposition;Helicase;Helitron-1` to `Class_II_DNA_Transposition;HUH_Transposase;Rolling_Circle;Helitron-1`
- DFC:0000020 Helitron-2: `Class_II_DNA_Transposition;Helicase;Helitron-2` to `Class_II_DNA_Transposition;HUH_Transposase;Rolling_Circle;Helitron-2`
- DFC:0000127 L1: `Class_I_Retrotransposition;LINE;Group-II;Group-1;L1-like;L1-group;L1` to `Class_I_Retrotransposition;LINE;Group-1;L1`
- DFC:0000128 Tx1: `Class_I_Retrotransposition;LINE;Group-II;Group-1;L1-like;L1-group;Tx1` to `Class_I_Retrotransposition;LINE;Group-1;Tx1`
- DFC:0000136 Deceiver: `Class_I_Retrotransposition;LINE;Group-II;Group-1;R4-like;Deceiver` to `Class_I_Retrotransposition;LINE;Group-2;Deceiver`
- DFC:0000137 Dong-R4: `Class_I_Retrotransposition;LINE;Group-II;Group-1;R4-like;Dong-R4` to `Class_I_Retrotransposition;LINE;Group-2;Dong-R4`
- DFC:0000138 RandI: `Class_I_Retrotransposition;LINE;Group-II;Group-1;R4-like;Dualen` to `Class_I_Retrotransposition;LINE;Group-2;RandI`
- DFC:0000142 CR1-group: `Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like;CR1-group` to `Class_I_Retrotransposition;LINE;Group-3;CR1-group`
- DFC:0000147 Rex-Babar: `Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like;CR1-group;Rex-Babar` to `Class_I_Retrotransposition;LINE;Group-3;Rex-Babar`
- DFC:0000148 R1-group: `Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like;R1-group` to `Class_I_Retrotransposition;LINE;Group-3;R1-group`
- DFC:0000149 I-group: `Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like;R1-group;I-group` to `Class_I_Retrotransposition;LINE;Group-3;I-group`
- DFC:0000155 Tad1: `Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like;Tad1` to `Class_I_Retrotransposition;LINE;Group-3;Tad1`
- DFC:0000018 Helentron: `Class_II_DNA_Transposition;Helicase;Helentron` to `Class_II_DNA_Transposition;HUH_Transposase;Rolling_Circle;Helitron-2;Helentron`
- DFC:0000054 ISL2EU: `Class_II_DNA_Transposition;Transposase;PIF-Harbinger;ISL2EU` to `Class_II_DNA_Transposition;DDE_Transposase;PIF-Harbinger;ISL2EU-group;ISL2EU`
- DFC:0000055 Spy: `Class_II_DNA_Transposition;Transposase;PIF-Harbinger;Spy` to `Class_II_DNA_Transposition;DDE_Transposase;PIF-Harbinger;ISL2EU-group;Spy`
- DFC:0000159 BovB: `Class_I_Retrotransposition;LINE;Group-II;Group-2;RTE-like;RTE-group;BovB` to `Class_I_Retrotransposition;LINE;Group-2;RTE-like;BovB`
- DFC:0000161 RTEX: `Class_I_Retrotransposition;LINE;Group-II;Group-2;RTE-like;RTE-group;RTE-X` to `Class_I_Retrotransposition;LINE;Group-2;RTE-like;RTEX`
- DFC:0000146 L2: `Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like;CR1-group;L2-group;L2` to `Class_I_Retrotransposition;LINE;Group-3;CR1-group;L2`
- DFC:0000153 LOA: `Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like;R1-group;R1-subgroup;LOA` to `Class_I_Retrotransposition;LINE;Group-3;R1-group;LOA`
- DFC:0000154 R1: `Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like;R1-group;R1-subgroup;R1` to `Class_I_Retrotransposition;LINE;Group-3;R1-group;R1`
- DFC:0000256 Caulimoviridae: `Class_I_Retrotransposition;Retrotransposon;Long_Terminal_Repeat_Element;Gypsy-ERV;Pararetroviridae;Caulimoviridae` to `Class_I_Retrotransposition;Retrotransposon;Long_Terminal_Repeat_Element;Gypsy-ERV;Caulimoviridae`

### Renamed

- DFC:0000017: Helicase to HUH_Transposase. The old label stays as a synonym.
- DFC:0000021: Transposase to DDE_Transposase. The old label stays as a synonym.
- DFC:0000026: CACTA to CMCT. The old label stays as a synonym.
- DFC:0000016: Maverick-Mavirus to Mavirus. The old label stays as a synonym.
- DFC:0000023: Academ-1 to AcademX. The old label stays as a synonym.
- DFC:0000025: Academ-H to AcademH. The old label stays as a synonym.
- DFC:0000138: Dualen to RandI. The old label stays as a synonym.
- DFC:0000161: RTE-X to RTEX. The old label stays as a synonym.
- DFC:0000227: Tad1_End to Tad1-end. The old label stays as a synonym.

### RepeatMasker label changed

- DFC:0000017 HUH_Transposase: RC to none. The term becomes a grouping.
- DFC:0000116 Ambal: LINE/CRE-Ambal to LINE/Ambal
- DFC:0000120 Odin: LINE/CRE-Odin to LINE/Odin
- DFC:0000132 Hero: LINE/R2-Hero to LINE/Hero
- DFC:0000019 Helitron-1: RC/Helitron to DNA/RC-Helitron1
- DFC:0000020 Helitron-2: RC/Helitron-2 to DNA/RC-Helitron2
- DFC:0000023 AcademX: DNA/Academ-1 to DNA/AcademX
- DFC:0000025 AcademH: DNA/Academ-H to DNA/AcademH
- DFC:0000138 RandI: LINE/Dualen to LINE/RandI
- DFC:0000018 Helentron: RC/Helentron to DNA/RC-Helentron
- DFC:0000161 RTEX: LINE/RTE-X to LINE/RTEX
- DFC:0000257 Retroviridae: LTR/Cassandra to none. The term becomes a grouping.
- DFC:0000284 TATE: Unknown/TATE to DIRS/TATE

### Families reassigned

The term stays and stops taking families.

- DFC:0000257 Retroviridae: its 254 Dfam 4.0 families go to DFC:0000258 Orthoretrovirinae.

### Merged

Each merged term is retired with `replaced_by`, and its families follow.

- DFC:0000287 Centromeric into DFC:0000286 Unknown (2 Dfam 4.0 families)
- DFC:0000289 Other into DFC:0000286 Unknown (124 Dfam 4.0 families)
- DFC:0000005 Pseudogene into DFC:0000300 Multicopy_RNA_Gene (0 Dfam 4.0 families)
- DFC:0000006 RNA into DFC:0000300 Multicopy_RNA_Gene (17 Dfam 4.0 families)
- DFC:0000122 Genie into DFC:0000117 CRE (6 Dfam 4.0 families)
- DFC:0000024 Academ-2 into DFC:0000025 AcademH (497 Dfam 4.0 families)
- DFC:0000118 CRE-1 into DFC:0000117 CRE (0 Dfam 4.0 families)
- DFC:0000119 CRE-2 into DFC:0000117 CRE (0 Dfam 4.0 families)
- DFC:0000125 DRE into DFC:0000128 Tx1 (47 Dfam 4.0 families)
- DFC:0000129 Zorro into DFC:0000127 L1 (54 Dfam 4.0 families)
- DFC:0000268 TRIM into DFC:0000251 Long_Terminal_Repeat_Element (4 Dfam 4.0 families)
- DFC:0000272 Chlamys into DFC:0000275 Naiad (1,753 Dfam 4.0 families)
- DFC:0000157 ORTE into DFC:0000156 RTE-like (237 Dfam 4.0 families)
- DFC:0000160 RTE into DFC:0000156 RTE-like (22,804 Dfam 4.0 families)
- DFC:0000144 Zenon into DFC:0000143 CR1 (14,368 Dfam 4.0 families)

### Retired groupings

These groupings held no families. Their members now sit elsewhere.

- DFC:0000115 Group-I (`Class_I_Retrotransposition;LINE;Group-I`); consider DFC:0000114 LINE
- DFC:0000121 Group-II (`Class_I_Retrotransposition;LINE;Group-II`); consider DFC:0000114 LINE
- DFC:0000124 L1-like (`Class_I_Retrotransposition;LINE;Group-II;Group-1;L1-like`); consider DFC:0000123 Group-1
- DFC:0000126 L1-group (`Class_I_Retrotransposition;LINE;Group-II;Group-1;L1-like;L1-group`); consider DFC:0000123 Group-1
- DFC:0000135 R4-like (`Class_I_Retrotransposition;LINE;Group-II;Group-1;R4-like`); consider DFC:0000139 Group-2
- DFC:0000141 R1-like (`Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like`); consider DFC:0000305 Group-3
- DFC:0000158 RTE-group (`Class_I_Retrotransposition;LINE;Group-II;Group-2;RTE-like;RTE-group`); consider DFC:0000156 RTE-like
- DFC:0000145 L2-group (`Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like;CR1-group;L2-group`); consider DFC:0000142 CR1-group
- DFC:0000152 R1-subgroup (`Class_I_Retrotransposition;LINE;Group-II;Group-2;R1-like;R1-group;R1-subgroup`); consider DFC:0000148 R1-group
- DFC:0000255 Pararetroviridae (`Class_I_Retrotransposition;Retrotransposon;Long_Terminal_Repeat_Element;Gypsy-ERV;Pararetroviridae`); consider DFC:0000253 Gypsy-ERV

### Membership revised

- DFC:0000123 Group-1: keeps L1 and R2-like (L1-like dissolves, Tx1 moves up); R4-like members and Proto-1 leave.
- DFC:0000139 Group-2: keeps RTE-like, gains Deceiver, Dong-R4 and RandI; R1-like members leave for Group-3.

### Synonyms and mappings

- Added 25 synonyms, among them the label of every renamed term and of every merged term that names its survivor's elements. Changed the scope of 1.
- Removed the 194 Repbase mappings, because Repbase merges into Dfam. The built `TEClasses.tsv` loses its `repbase_equiv` column.
- Left the Wicker, Curcio-Derbyshire and Piegu mappings on the terms they were written for, retired terms included.

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
