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
	pip install pipenv==3.3.5
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
	.venv/bin/pip install git+git://github.com/PyCQA/pylint.git@e0fdd25c214e60bef10fbaa46252f4aaa74de8c2
	.venv/bin/pip install git+git://github.com/PyCQA/astroid.git@4e7d9fee4080d2e0db67a3e0463be8b196e56a95
	@ mkdir -p tmp
	@ touch $@

.PHONY: clean
clean:
	rm -rf $(ENV)
	rm -rf $(TMP)

# RUNTIME DEPENDENCIES #########################################################

.PHONY: data
data: install
	$(MANAGE) gendata
	$(MANAGE) addsongs
	$(MANAGE) updatesongs
	$(MANAGE) cleansongs

.PHONY: db
db:
	- createdb virtualboombox_dev

.PHONY: db-migrate
db-migrate: install
	$(MANAGE) migrate

.PHONY: db-superuser
db-superuser: install
	@ echo "Creating the default superuser..."
	@- echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@localhost', 'password')" | $(MANAGE) shell >> tmp/manage.log 2>&1

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
run: .envrc install db db-migrate db-superuser
	$(MANAGE) runserver 5000

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
