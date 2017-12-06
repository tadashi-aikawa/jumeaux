:PHONY release
release:
	@echo 'Recreate `jumeaux/__init__.py`'
	@echo "__version__ = '$(version)'" > jumeaux/__init__.py
	
	@echo 'Recreate `Dockerfile`'
	@cat template/Dockerfile | sed -r 's/VERSION/$(version)/g' > Dockerfile
	
	@echo 'Build documentation'
	@pipenv run mkdocs build
	
	@echo 'Staging and commit'
	@git add jumeaux/__init__.py
	@git add Dockerfile
	@git add docs
	@git commit -m ':package: Version $(version)'
	
	@echo 'Tags'
	@git tag $(version) -m $(version)
	
	@echo 'Success All!!'
	@echo 'Now you should only do `git push`!!'

