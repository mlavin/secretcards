KEY=$(shell strings /dev/urandom | grep -o '[[:alnum:]]' | head -n 64 | tr -d '\n';)

default: lint test

.env:
	@echo SECRET_KEY="$(KEY)" >> $@

install: .env
	pip install -r requirements.txt

lint: lint-py lint-migrations lint-django lint-deploy

lint-py:
	flake8 .

lint-migrations:
	@python manage.py makemigrations --dry-run | grep 'No changes detected' || (echo 'There are changes which require migrations.' && exit 1)

lint-django:
	@python manage.py check | grep 'System check identified no issues' || (echo 'Django has identified system issues.' && exit 1)

lint-deploy:
	@DEBUG=off SSL=on python manage.py check --deploy | grep 'System check identified no issues' || (echo 'Django has identified deployment issues.' && exit 1)

test:
	coverage run manage.py test
	coverage report -m --fail-under 90

.PHONY: default install test lint lint-py lint-migrations lint-django lint-deploy

.PRECIOUS: .env
