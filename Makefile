# Makefile to help automate tasks
WD := $(shell pwd)
PY := bin/python
PEP8 := bin/pep8
NOSE := bin/nosetests

.PHONY: clean_all
clean_all: clean_venv

# ###########
# Tests rule!
# ###########
.PHONY: test
test: venv develop $(NOSE)
	$(NOSE) --with-id -s -x src/bookie_api/tests

$(NOSE):
	$(PY) setup.py test

# #######
# INSTALL
# #######
.PHONY: all
all: venv deps develop

.PHONY: deps
deps: venv
	@echo "\n\nSilently installing packages (this will take a while)..."

venv: bin/python
bin/python:
	virtualenv .

.PHONY: clean_venv
clean_venv:
	rm -rf lib include local bin

develop: lib/python*/site-packages/bookie-api.egg-link
lib/python*/site-packages/bookie-api.egg-link:
	$(PY) setup.py develop


# ###########
# Development
# ###########

