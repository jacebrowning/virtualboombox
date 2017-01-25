.PHONY: install
install:
	pipenv install

.PHONY: data
data:
	@ echo "TODO: make data"

.PHONY: run
run: install
	heroku local
