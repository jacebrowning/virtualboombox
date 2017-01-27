.PHONY: all
all: install

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: setup
setup:
	python -m pip install --upgrade  pipenv
	@ touch Pipfile # force reinstall with the newer version of pipenv

.PHONY: doctor
doctor:
	@ python -m pip install verchew > /dev/null
	python -m verchew

# PROJECT DEPENDENCIES #########################################################

ENV := .venv
BIN := $(ENV)/bin
PYTHON := $(BIN)/python

.PHONY: install
install: $(ENV)
$(ENV): Pipfile Pipfile.lock
	pipenv install --dev
	@ touch $@

.PHONY: clean
clean:
	rm -rf $(ENV)

# RUNTIME DEPENDENCIES #########################################################

MANAGE := $(PYTHON) manage.py

.PHONY: data
data:
	- createdb virtualboombox_dev

.PHONY: migrate
migrate: install
	$(MANAGE) migrate

# VALIDATION TARGETS ###########################################################

PYTEST := $(BIN)/pytest

.PHONY: test
test: install
	$(PYTEST)

# DEVELOPMENT TARGETS ##########################################################

ACIVATE := . $(BIN)/activate

.PHONY: run
run: install data migrate
	$(MANAGE) runserver

.PHONY: run-prod
run-prod: .env install data migrate
	$(MANAGE) collectstatic --no-input
	$(ACIVATE) && heroku local

.env:
	echo SECRET_KEY=prod >> $@
	echo DATABASE_URL=postgresql://localhost/virtualboombox_dev >> $@
