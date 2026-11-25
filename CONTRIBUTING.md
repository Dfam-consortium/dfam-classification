# Changing the classification

`main` always holds the version being prepared. A release is a tag on
`main`, such as `v2.0.0`. Nothing reaches `main` except through a pull
request that passes validation.

## Proposing a change

Open an issue with the "Term request or change" template, or go straight
to a pull request if the change is already agreed.

## Making a change

1. Branch from `main`.
2. Edit `terms.tsv`, `mappings.sssom.tsv` or `synonyms.tsv` as the README
   describes. Run `make ids` for new terms.
3. If this is the first change since a release, raise `VERSION` by the
   rule in `docs/design.md` section 7 and start a new section in
   `CHANGELOG.md`. If a later change needs a bigger bump than the one
   already made (a retirement after a new term, say), raise it again.
   When `VERSION` changes before release, change `created_in` and
   `obsoleted_in` on the rows added since the last release to match.
4. Add a line to the `CHANGELOG.md` section saying what changed and why.
   For a merge, split or retirement, give the number of Dfam families on
   the retired term.
5. Run `make` and `make check-previous`.
6. Open a pull request. One classification decision per pull request is
   easiest to review, since the diff of `terms.tsv` is then a few rows.

The checks on a pull request run the same two `make` targets and keep
the built `TEClasses.tsv` and `paths.tsv` as a downloadable artifact.

## Identifiers before a release

An ID is permanent once a release contains it. `make check-previous`
enforces that: no released ID may disappear, and its `created_in` may not
change. An ID issued since the last release is still provisional. If the
term is dropped before the release, delete the row; the number stays
spent, because `last-id` never goes down.

## Releasing

1. Check that `VERSION` and the `CHANGELOG.md` heading agree and that the
   changelog lists every change since the last tag
   (`git diff v1.0.0 -- terms.tsv` shows them).
2. Run `make check-previous` and `make release-files` on `main`. The
   second copies the built `TEClasses.tsv` and `paths.tsv` into
   `releases/2.0.0/`. Commit that directory through a pull request. The
   next version's build reads `paths.tsv` from it, which is how
   `paths.tsv` keeps every path any release has used.
3. Tag that commit and push: `git tag -a v2.0.0 -m "Dfam classification
   2.0.0"`, then `git push origin v2.0.0`. The release workflow checks
   the tag against `VERSION`, rebuilds, checks that `releases/2.0.0/`
   matches the build, and publishes a GitHub release with
   `TEClasses.tsv`, `paths.tsv` and the three source files attached.
4. Load the release into Dfam in the order given in `docs/design.md`
   section 8.

A released tag is never moved. A mistake found after release is fixed in
the next patch version.
