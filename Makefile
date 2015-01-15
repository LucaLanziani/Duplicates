.PHONY: TEST ENV

ENV: Makefile
	virtualenv --distribute ./env

PYPY_ENV:
	virtualenv -p /usr/bin/pypy --distribute ./pypy_env

CHECK_ENV:
ifndef VIRTUAL_ENV
	$(error PLEASE ENTER THE VIRTUALENV BEFORE FUN THE COMMAND)
endif

UPDATE_ENV: CHECK_ENV requirements.txt
	pip install --upgrade setuptools
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .  # install the duplicates package locally

TESTS: CHECK_ENV
	nosetests

FLAKE8: CHECK_ENV
	flake8