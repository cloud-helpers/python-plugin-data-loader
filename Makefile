#
# File: https://github.com/cloud-helpers/python-plugin-data-loader/blob/main/Makefile
#
# Doc:
# * https://medium.com/@Nexumo_/uv-for-python-reproducible-envs-that-dont-break-ci-8bc7104866cd
#

#
PACKAGE_NAME := "data-loader-plugin"
$(eval PACKAGE_NAME_UNDERSCORES=$(shell echo $(PACKAGE_NAME) | tr - _))
PYPI_USER := "$PYPI_USER"
PYPI_TOKEN := "$PYPI_TOKEN"
COVERAGE_OPTIONS := "--cov-branch --cov-config coverage/.coveragerc --cov-report term --cov-report html"
NOW_TS := $(shell TZ=":Europe/Paris" date '+%Y-%m-%d %H:%M:%S %Z')
TODAY_DATE := $(shell TZ=":Europe/Paris" date '+%Y-%m-%d')

## HELP

.DEFAULT_GOAL:=help

.PHONY: info tests

help: ## Display the help menu.
	@echo "make <target>"
	@echo "Environments: $(ENV_TGTS)"
	@grep -h "\#\#" $(MAKEFILE_LIST)

clean-python:
	@rm -rf .venv .mypy_cache __pycache__

clean-dist:
	@rm -rf dist

clean-log:
	@rm -f *.log

clean: clean-python clean-dist clean-log

init:
	@uv lock
	@uv export --format requirements.txt > requirements.txt

update:
	@uv sync
	@uv export --format requirements.txt > requirements.txt

build: clean-dist
	@uv build
	@ls -lFh dist/

# --force-reinstall
install-local: uninstall-local
	$(eval PACKAGE_VERSION=$(shell cat VERSION))
	@python -mpip install dist/$(PACKAGE_NAME_UNDERSCORES)-$(PACKAGE_VERSION)-*.whl

uninstall-local:
	$(eval PACKAGE_VERSION=$(shell cat VERSION))
	@python -mpip uninstall -y $(PACKAGE_NAME)

code-format:
	@ruff check --fix src
	@ruff format src

code-quality-mypy:
	@uv run mypy src

code-quality-ty:
	@ty check src

tests:
	@uv run pytest tests

# Bumpers

bump-version: ## Bump the version into the other files from the VERSION file
	$(eval PACKAGE_VERSION=$(shell cat VERSION))
	sed -i.bak 's/^version = .*/version = "$(PACKAGE_VERSION)"/' pyproject.toml && rm pyproject.toml.bak
	@echo "Next step: make init update"

increment-dev-version:
	$(eval VERSION=$(shell cat VERSION))
	@VERSION_REGEX="^[0-9]+\.[0-9]+\.[0-9]+$$"; \
	DEV_VERSION_REGEX="^[0-9]+\.[0-9]+\.[0-9]+\.dev[0-9]+$$"; \
	echo "Current version: $(VERSION)"; \
	if echo "$(VERSION)" | grep -Eq "$$VERSION_REGEX"; then \
		NEW_VERSION=$$(echo "$(VERSION)" | awk -F. '{print $$1"."$$2+1".0.dev0"}'); \
		echo "Updating release version to the next minor dev version: $$NEW_VERSION"; \
	elif echo "$(VERSION)" | grep -Eq "$$DEV_VERSION_REGEX"; then \
		NEW_VERSION=$$(echo "$(VERSION)" | awk -F'.dev' '{print $$1".dev"($$2+1)}'); \
		echo "Updating dev version to: $$NEW_VERSION"; \
	else \
		echo "ERROR: Version format is invalid. Should be X.Y.Z or X.Y.Z.devN"; \
		exit 1; \
	fi; \
	echo "$$NEW_VERSION" > VERSION

switch-to-minor-version:
	$(eval VERSION=$(shell cat VERSION))
	@VERSION_REGEX="^[0-9]+\.[0-9]+\.[0-9]+\.dev[0-9]+$$"; \
	echo "Current version: $(VERSION)"; \
	if echo "$(VERSION)" | grep -Eq "$$VERSION_REGEX"; then \
		NEW_VERSION=$$(echo "$(VERSION)" | sed 's/\.dev[0-9]*//'); \
		echo "Switching to next minor version: $$NEW_VERSION"; \
	else \
		echo "ERROR: Version format is invalid. Should be X.Y.Z.devN"; \
		exit 1; \
	fi; \
	echo "$$NEW_VERSION" > VERSION

bump-to-minor-version:
	$(eval VERSION=$(shell cat VERSION))
	@VERSION_REGEX="^[0-9]+\.[0-9]+\.[0-9]+\.dev[0-9]+$$"; \
	echo "Current version: $(VERSION)"; \
	if echo "$(VERSION)" | grep -Eq "$$VERSION_REGEX"; then \
		NEW_VERSION=$$(echo "$(VERSION)" | sed 's/\.dev[0-9]*//'); \
		echo "Bumping to next minor version: $$NEW_VERSION"; \
	else \
		echo "ERROR: Version format is invalid. Should be X.Y.Z.devN"; \
		exit 1; \
	fi; \
	echo "$$NEW_VERSION" > VERSION


bump-to-major-version:
	$(eval VERSION=$(shell cat VERSION))
	@VERSION_REGEX="^[0-9]+\.[0-9]+\.[0-9]+(\.dev[0-9]+)?(\+[a-zA-Z0-9._-]+)?$$"; \
	echo "Current version: $(VERSION)"; \
	if echo "$(VERSION)" | grep -Eq "$$VERSION_REGEX"; then \
		NEW_VERSION=$$(echo "$(VERSION)" | sed 's/\(\.dev[0-9]*\)\?(\+[a-zA-Z0-9._-]*)\?//g'); \
		NEW_VERSION=$$(echo "$$NEW_VERSION" | awk -F'[.]' '{print $$1+1".0.0"}'); \
		echo "Bumping version to next major: $$NEW_VERSION"; \
	else \
		echo "ERROR: Version format is invalid. Should be X.Y.Z, X.Y.Z.devN, X.Y.Z+branch.name, or X.Y.Z.devN+branch.name"; \
		exit 1; \
	fi; \
	echo "$$NEW_VERSION" > VERSION

bump-to-patch-version:
	$(eval VERSION=$(shell cat VERSION))
	@VERSION_REGEX="^[0-9]+\.[0-9]+\.[0-9]+(\.dev[0-9]+)?(\+[a-zA-Z0-9._-]+)?$$"; \
	echo "Current version: $(VERSION)"; \
	if echo "$(VERSION)" | grep -Eq "$$VERSION_REGEX"; then \
		NEW_VERSION=$$(echo "$(VERSION)" | sed 's/\(\.dev[0-9]*\)\?(\+[a-zA-Z0-9._-]*)\?//g'); \
		NEW_VERSION=$$(echo "$$NEW_VERSION" | awk -F'[.]' '{print $$1"."$$2"."$$3+1}'); \
		echo "Bumping version to next patch: $$NEW_VERSION"; \
	else \
		echo "ERROR: Version format is invalid. Should be X.Y.Z, X.Y.Z.devN, X.Y.Z+branch.name, or X.Y.Z.devN+branch.name"; \
		exit 1; \
	fi; \
	echo "$$NEW_VERSION" > VERSION


