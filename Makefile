.PHONY: TEST ENV

ENV: Makefile
	virtualenv --distribute ./env

CHECK_ENV:
ifndef VIRTUAL_ENV
	$(error PLEASE ENTER THE VIRTUALENV BEFORE FUN THE COMMAND)
endif

UPDATE_ENV: CHECK_ENV requirements.txt
	pip install --upgrade setuptools
	pip install --upgrade pip
	pip install -r requirements.txt

TEST: CHECK_ENV
	nosetests
