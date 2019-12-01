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

version := $(shell git rev-parse --abbrev-ref HEAD)


#---- Basic

init-dev: ## Install dependencies and create envirionment
	@poetry install

start-api: ## Start dummy API
	@poetry run python jumeaux/executor.py server &

stop-api: ## Stop dummy API
	@pkill -f 'jumeaux/executor.py server'

test: ## Test
	@poetry run python -m pytest -vv --cov-report=xml --cov=. tests/

test-cli: ## Test on CLI
	@echo Start $@
	@make start-api 2> /dev/null
	@poetry run bats test.bats
	@make stop-api
	@echo End $@

clear: ## Remove responses, requests, api and config.yml
	@rm -rf responses requests api config.yml


#---- Docs

serve-docs: ## Build and serve documentation
	@poetry run mkdocs serve -a 0.0.0.0:8000


#---- Release

_clean-package-docs: ## Clean package documentation
	@rm -rf docs/*

package-docs: _clean-package-docs ## Package documentation
	@poetry run mkdocs build

_clean-package: ## Clean package
	@rm -rf build dist jumeaux.egg-info

_package: _clean-package ## Package OwlMixin
	@poetry build -f wheel

release: package-docs ## Release

	@echo '0. Install packages from lockfile and test'
	@make init-dev
	@make test
	@make test-cli

	@echo '1. Version up'
	@poetry version $(version)
	@echo "__version__ = '$(version)'" > jumeaux/__init__.py

	@echo '2. Recreate `Dockerfile`'
	@cat template/Dockerfile | sed -r 's/VERSION/$(version)/g' > Dockerfile

	@echo '3. Staging and commit'
	git add jumeaux/__init__.py Dockerfile docs pyproject.toml
	git commit -m ':package: Version $(version)'

	@echo '4. Tags'
	git tag v$(version) -m v$(version)

	@echo '5. Package Jumeaux'
	@make _package

	@echo '6. Publish'
	@poetry publish

	@echo '7. Push'
	git push origin v$(version)
	git push

	@echo 'Success All!!'
	@echo 'Create a pull request and merge to master!!'
	@echo 'https://github.com/tadashi-aikawa/jumeaux/compare/$(version)?expand=1'

