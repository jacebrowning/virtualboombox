.PHONY: all
all: install

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: setup
setup:
	python -m pip install --upgrade verchew pipenv
	@ touch Pipfile # force reinstall with the newer version of pipenv
	python -m verchew

# PROJECT DEPENDENCIES #########################################################

ENV := .venv
BIN := $(ENV)/bin

.PHONY: install
install: $(ENV)
$(ENV): Pipfile Pipfile.lock
	pipenv install --dev
	@ touch $@

.PHONY: clean
clean:
	rm -rf $(ENV)

# RUNTIME DEPENDENCIES #########################################################

.PHONY: data
data:
	@ echo "TODO: make data"

# VALIDATION TARGETS ###########################################################

.PHONY: test
test: install
	pipenv run pytest

# DEVELOPMENT TARGETS ##########################################################

ACIVATE := . $(BIN)/activate

.PHONY: run
run: install
	$(ACIVATE) && heroku local
