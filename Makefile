MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: $(shell egrep -oh ^[a-zA-Z0-9][a-zA-Z0-9_-]+: $(MAKEFILE_LIST) | sed 's/://')

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9][a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "[REQUIRED ERROR] \`$*\` is required."; \
		exit 1; \
	fi

-include .env

#---- Basic

server: ## Start dummy API
	@uv run python jumeaux/main.py server

viewer: ## Start Jumeaux Viewer
	@uv run python jumeaux/main.py viewer

lint: ## Lint
	@shopt -s globstar; uv run ruff check jumeaux/**/*.py

format: ## Format
	@shopt -s globstar; uv run ruff format jumeaux/**/*.py

test: ## Test
	@uv run python -m pytest -vv --cov-report=xml --cov=. tests/

test-e2e: ## Test on CLI
	@uv run python -m pytest -vv e2e/main.py

ci: ## lint & format & test & test-e2e
	@make lint && make format && make test && make test-e2e

clear: ## Remove responses, requests, api and config.yml
	@rm -rf responses requests api config.yml


#---- Docs

serve-docs: ## Build and serve documentation
	@uv run mkdocs serve -a localhost:8000


#---- Release

_clean-package-docs: ## Clean package documentation
	@rm -rf docs/*

package-docs: _clean-package-docs ## Package documentation
	@uv run mkdocs build

_clean-package: ## Clean package
	@rm -rf build dist jumeaux.egg-info

_package: _clean-package ## Package Jumeaux
	@uv build

release: guard-version ## make release version=x.y.z
	@echo '0. Install packages from lockfile, then test and package documentation'
	@uv sync
	@make test test-e2e package-docs

	@echo '1. Version up'
	@sed -i 's/^version = ".*"/version = "$(version)"/' pyproject.toml
	@echo "__version__ = '$(version)'" > jumeaux/__init__.py

	@echo '2. Staging and commit'
	git add jumeaux/__init__.py docs pyproject.toml
	git commit -m '📦 Version $(version)'

	@echo '3. Tags'
	git tag v$(version) -m v$(version)

	@echo '4. Package Jumeaux'
	@make _package

	@echo '5. Publish'
	@uv publish

	@echo '6. Push'
	git push --tags
	git push

	@echo 'Success All!!'

