.PHONY: all
all: install

.PHONY: ci
ci: check test

ENV := .venv
TMP := tmp

MANAGE := pipenv run python manage.py

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: setup
setup:
	python -m pip install pipenv==3.3.4
	@ touch Pipfile # force reinstall with the newer version of pipenv

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
data: install
	$(MANAGE) gendata
	$(MANAGE) addsongs

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
