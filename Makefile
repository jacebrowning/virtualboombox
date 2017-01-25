.PHONY: all
all: install

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: setup
setup:
	python -m pip install --upgrade verchew pipenv
	python -m verchew

# PROJECT DEPENDENCIES #########################################################

ENV := .venv
BIN := $(ENV)/bin

.PHONY: install
install:
	pipenv install --dev

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
