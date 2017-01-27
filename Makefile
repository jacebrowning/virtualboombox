.PHONY: all
all: install

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: setup
setup:
	python -m pip install --upgrade  pipenv
	@ touch Pipfile # force reinstall with the newer version of pipenv

.PHONY: doctor
doctor:
	bin/verchew

# PROJECT DEPENDENCIES #########################################################

ENV := .venv
BIN := $(ENV)/bin
PYTHON := $(BIN)/python
ACIVATE := . $(BIN)/activate &&

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
	@ echo "TODO: generate sample data"

.PHONY: db
db:
	- createdb virtualboombox_dev

.PHONY: db-migrate
db-migrate: install
	$(MANAGE) migrate

.PHONY: db-superuser
db-superuser: install
	- echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@localhost', 'password')" | $(MANAGE) shell

# VALIDATION TARGETS ###########################################################

PYTEST := $(BIN)/pytest
PYTEST_WATCH := $(BIN)/ptw

.PHONY: test
test: install
	$(PYTEST)

.PHONY: watch
watch: install
	$(ACIVATE) $(PYTEST_WATCH)

# SERVER TARGETS ###############################################################

.PHONY: run
run: install db db-migrate db-superuser
	$(MANAGE) runserver

.PHONY: run-prod
run-prod: .env install db
	$(ACIVATE) bin/post_compile
	$(ACIVATE) heroku local

.env:
	echo SECRET_KEY=prod >> $@
	echo DATABASE_URL=postgresql://localhost/virtualboombox_dev >> $@
