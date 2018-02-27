MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
ARGS :=
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: $(shell egrep -oh ^[a-zA-Z0-9][a-zA-Z0-9_-]+: $(MAKEFILE_LIST) | sed 's/://')

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9][a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

version := $(shell git rev-parse --abbrev-ref HEAD)

#------

init: ## Intialize develop environment
	@echo Start $@
	@pipenv install -d
	@echo End $@

run-init: ## Run jumeaux init
	@echo Start $@
	@pipenv run python jumeaux/executor.py init $(ARGS)
	@echo End $@

run: ## Run jumeaux run
	@echo Start $@
	@pipenv run python jumeaux/executor.py run $(ARGS)
	@echo End $@

retry: ## Retry jumeaux
	@echo Start $@
	@pipenv run python jumeaux/executor.py retry $(ARGS)
	@echo End $@

serve-docs: ## Build and serve documentation
	@echo Start $@
	@pipenv run mkdocs serve -a 0.0.0.0:8000
	@echo End $@

_clean-package-docs: ## Clean package documentation
	@rm -rf docs/*

package-docs: _clean-package-docs ## Package documentation
	@echo Start $@
	@pipenv run mkdocs build
	@echo End $@

_clean-package: ## Clean package
	@echo Start $@
	@rm -rf build dist jumeaux.egg-info
	@echo End $@

_package: _clean-package ## Package OwlMixin
	@echo Start $@
	@pipenv run python setup.py bdist_wheel
	@echo End $@

test: ## Test
	@echo Start $@
	@pipenv run pytest $(ARGS)
	@echo End $@

release: init test package-docs ## Release (set TWINE_USERNAME and TWINE_PASSWORD to enviroment varialbles)
	@echo '1. Recreate `jumeaux/__init__.py`'
	@echo "__version__ = '$(version)'" > jumeaux/__init__.py

	@echo '2. Recreate `Dockerfile`'
	@cat template/Dockerfile | sed -r 's/VERSION/$(version)/g' > Dockerfile

	@echo '3. Staging and commit'
	git add jumeaux/__init__.py
	git add Dockerfile
	git add mkdocs/ja/releases/index.md
	git add docs
	git commit -m ':package: Version $(version)'

	@echo '4. Tags'
	git tag $(version) -m $(version)

	@echo '5. Push'
	git push

	@echo '6. Deploy'
	@echo 'Packageing...'
	@pipenv run python setup.py bdist_wheel
	@echo 'Deploying...'
	@pipenv run twine upload dist/jumeaux-$(version)-py3-none-any.whl

	@echo 'Success All!!'
	@echo 'Now you should only do `git push`!!'

