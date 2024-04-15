.PHONY: install
install:
	poetry install --no-root

#.PHONY: install-pre-commit
#install-pre-commit:
#	poetry run pre-commit uninstall; poetry run pre-commit install

#.PHONY: lint
#lint:
#	poetry run pre-commit run

.PHONY: migrate
migrate:
	poetry run python3 core/manage.py migrate

.PHONY: migrations
migrations:
	poetry run python3 core/manage.py makemigrations

.PHONY: run-server
run-server:
	poetry run python3 core/manage.py runserver

.PHONY: shell
shell:
	poetry run python3 core/manage.py shell

.PHONY: superuser
superuser:
	poetry run python3 core/manage.py createsuperuser

.PHONY: test
test:
	poetry run pytest core

.PHONY: update
update: install migrate install-pre-commit ;

.PHONY: docker-project
docker-project:
	docker-compose up -d --build; docker ps