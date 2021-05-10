##############################################################################################
# SETUP                                                                                      #
##############################################################################################


SOURCE_FOLDER = pybokio
PYTHON ?= python3


##############################################################################################
# PROJECT SETUP                                                                              #
##############################################################################################


.PHONY: env
env:
	$(PYTHON) -m venv .venv --prompt $(SOURCE_FOLDER)

.PHONY: env-update
env-update:
	bash -c ". .venv/bin/activate; pip install --upgrade -r requirements.txt"


##############################################################################################
# BASIC COMMANDS                                                                             #
##############################################################################################


.PHONY: clean
clean:
	rm -f .gitinfo
	rm -rf build dist *.egg-info
	find $(SOURCE_FOLDER) -name __pycache__ | xargs rm -rf
	find $(SOURCE_FOLDER) -name '*.pyc' -delete
	rm -rf reports .coverage
	rm -rf docs/build docs/source
	rm -rf .*cache

.PHONY: check
check: check-imports check-code

.PHONY: check-imports
check-imports:
	isort --check-only $(SOURCE_FOLDER) tests/*
	vulture

.PHONY: check-code
check-code:
	black --check $(SOURCE_FOLDER) tests/*

.PHONY: reformat
reformat:
	isort --atomic $(SOURCE_FOLDER) tests/*
	black $(SOURCE_FOLDER) tests/*

.PHONY: tests
tests:
	pytest tests/

.PHONY: tests-unit
tests-unit:
	pytest tests/unit/

.PHONY: tests-integration
tests-integration:
	pytest tests/integration/

.PHONY: coverage
coverage:
	pytest --cov=$(SOURCE_FOLDER) tests/


##############################################################################################
# BUILDING & PUBLISHING                                                                      #
##############################################################################################


.PHONY: build
build:
	python setup.py --quiet sdist bdist_wheel

.PHONY: publish-test
publish-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: publish
publish:
	twine upload dist/*

.PHONY: build-publish
build-publish: clean build publish
	python setup.py --quiet sdist bdist_wheel


##############################################################################################
# VERSIONING                                                                                 #
##############################################################################################


.PHONY: version
version:
	python -c "import $(SOURCE_FOLDER); print($(SOURCE_FOLDER).__version__)"


.PHONY: bump-version-patch
bump-version-patch:
	# Note: You should only run this on a clean working copy
	#       If this operation succeeds, it will create a version-bumping commit
	bump2version patch --list
	git log --oneline -1


.PHONY: bump-version-minor
bump-version-minor:
	# Note: You should only run this on a clean working copy
	#       If this operation succeeds, it will create a version-bumping commit
	bump2version minor --list
	git log --oneline -1

.PHONY: bump-version-major
bump-version-major:
	# Note: You should only run this on a clean working copy
	#       If this operation succeeds, it will create a version-bumping commit
	bump2version major --list
	git log --oneline -1
