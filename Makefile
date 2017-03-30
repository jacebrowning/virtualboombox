.PHONY: all
all: install

.PHONY: ci
ci: check test

export PIPENV_SHELL_COMPAT=true
export PIPENV_VENV_IN_PROJECT=true

ENV := .venv
TMP := tmp

MANAGE := pipenv run python manage.py

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: setup
setup:
	pip install pipenv==3.5.0
	pipenv lock
	touch Pipfile

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
data: install
	$(MANAGE) gendata
	$(MANAGE) syncdata --limit=10
endif

.PHONY: db
db:
	- createdb virtualboombox_dev

.PHONY: migrate
migrate: install
	$(MANAGE) migrate

# VALIDATION TARGETS ###########################################################

.PHONY: check
check: install
	pipenv run pylint api player virtualboombox --rcfile=.pylint.ini
	pipenv run pycodestyle --config=.pycodestyle.ini

.PHONY: test
test: install
	pipenv run py.test

.PHONY: watch
watch: install
	pipenv run ptw

.PHONY: coverage
coverage: install
	pipenv run coverage.space jacebrowning/virtualboombox overall

# SERVER TARGETS ###############################################################

.PHONY: run
run: .envrc install db migrate
	$(MANAGE) runserver 5000

.PHONY: reload
reload: .envrc install
	$(MANAGE) livereload

.PHONY: run-prod
run-prod: .envrc install db
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
