.PHONY: all
all: install

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: setup
setup:
	python -m pip install verchew==1.1b.1
	python -m pip install pipenv==3.1.9
	python -m verchew

# PROJECT DEPENDENCIES #########################################################

.PHONY: install
install:
	pipenv install --dev

.PHONY: clean
clean:
	rm -rf .venv

# RUNTIME DEPENDENCIES #########################################################

.PHONY: data
data:
	@ echo "TODO: make data"

# VALIDATION TARGETS ###########################################################

.PHONY: test
test: install
	pipenv run pytest

# DEVELOPMENT TARGETS ##########################################################

.PHONY: run
run: install
	heroku local
