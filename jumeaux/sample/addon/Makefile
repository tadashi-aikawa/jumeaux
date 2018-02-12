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

#------

init: ## Intialize develop environment
	@echo Start $@
	@pipenv install -d
	@pipenv run jumeaux init rest
	@echo End $@

run: ## Run jumeaux
	@echo Start $@
	@PYTHONPATH=`pwd` pipenv run jumeaux run $(ARGS)
	@echo End $@

test: ## Test
	@echo Start $@
	@pipenv run pytest $(ARGS)
	@echo End $@

