.PHONY: all
all: install

.PHONY: ci
ci: check test

export PIPENV_SHELL_COMPAT=true
export PIPENV_VENV_IN_PROJECT=true

ENV := .venv
TMP := tmp

RUN := pipenv run
MANAGE := $(RUN) python manage.py

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: doctor
doctor:
	bin/verchew

# PROJECT DEPENDENCIES #########################################################

.PHONY: install
install: $(ENV)
$(ENV): Pipfile*
	pipenv install --dev
	@ mkdir -p tmp
	@ touch $@

.PHONY: clean
clean:
	rm -rf $(ENV)
	rm -rf $(TMP)

# RUNTIME DEPENDENCIES #########################################################

.PHONY: data
ifdef VIRTUAL_ENV
data:
	python manage.py gendata
	python manage.py syncdata
else
data: install migrate
	$(MANAGE) gendata
	$(MANAGE) syncdata --limit=10
endif

.PHONY: migrate
migrate: install
	$(MANAGE) migrate

# VALIDATION TARGETS ###########################################################

.PHONY: check
check: install
	$(RUN) pylint api player social virtualboombox --rcfile=.pylint.ini
	$(RUN) pycodestyle --config=.pycodestyle.ini

.PHONY: test
test: install
	$(RUN) pytest

.PHONY: watch
watch: install
	$(RUN) ptw

.PHONY: coverage
coverage: install
	$(RUN) coveragespace jacebrowning/virtualboombox overall

# SERVER TARGETS ###############################################################

.PHONY: run
run: .envrc install
	$(RUN) honcho start --procfile=Procfile.dev --port=$${PORT:-8000}

.PHONY: run-prod
run-prod: .envrc install
	pipenv shell -c "bin/pre_compile; exit $$?"
	pipenv shell -c "bin/post_compile; exit $$?"
	pipenv shell -c "heroku local; exit $$?"

.envrc:
	echo export SECRET_KEY=prod >> $@
	echo export DATABASE_URL=postgresql://localhost/virtualboombox_dev >> $@
	echo export LASTFM_API_KEY= >> $@
	echo export LASTFM_API_SECRET= >> $@
	echo export GOOGLE_APPLICATION_CREDENTIALS_DATA= >> $@
	echo export GOOGLE_APPLICATION_CREDENTIALS=tmp/google.json >> $@
	echo export YOUTUBE_API_KEY= >> $@
	echo export VIRTUALBOOMBOX_MINIMUM_SONGS=250 >> $@
