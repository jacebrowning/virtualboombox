.PHONY: all
all: install

.PHONY: install
install:
	pipenv install --dev

.PHONY: data
data:
	@ echo "TODO: make data"

.PHONY: test
test: install
	pipenv run pytest

.PHONY: run
run: install
	heroku local

.PHONY: clean
clean:
	rm -rf .venv
