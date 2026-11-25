PYTHON ?= python3
COUNTS ?= stats/dfam-4.0-family-counts.tsv
VERSION := $(shell cat VERSION)
# The newest release kept in releases/, other than the version being
# prepared. Its paths.tsv carries the path history forward.
PREVIOUS := $(shell ls releases 2>/dev/null | grep -vx '$(VERSION)' | sort -V | tail -1)
PREVIOUS_ARGS := $(if $(PREVIOUS),--previous-paths releases/$(PREVIOUS)/paths.tsv --previous-version $(PREVIOUS))

.PHONY: all validate build roundtrip check-previous release-files ids clean

all: validate build

validate:
	$(PYTHON) scripts/validate.py

build: validate
	$(PYTHON) scripts/build.py --counts $(COUNTS) $(PREVIOUS_ARGS)

# Only meaningful for 1.0.0, whose content matches the Dfam 4.0 file.
roundtrip: build
	$(PYTHON) scripts/check_roundtrip.py

# No term of the last release may have disappeared. Looks for the newest
# release tag before this commit, so it also works on a tagged commit.
check-previous:
	@mkdir -p build; \
	prev=$$(git describe --tags --abbrev=0 --match 'v[0-9]*' --exclude '*-*' HEAD^ 2>/dev/null); \
	if [ -z "$$prev" ]; then echo "no earlier release tag; nothing to compare"; exit 0; fi; \
	git show "$$prev:terms.tsv" > build/previous-terms.tsv && \
	echo "comparing with $$prev" && \
	$(PYTHON) scripts/validate.py --previous build/previous-terms.tsv

# Keep the built files of the version being released. Commit them
# before tagging; the next version's build reads paths.tsv from here.
release-files: build
	mkdir -p releases/$(VERSION)
	cp build/TEClasses.tsv build/paths.tsv releases/$(VERSION)/

ids:
	$(PYTHON) scripts/assign_ids.py

clean:
	rm -rf build
