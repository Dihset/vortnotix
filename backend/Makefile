.PHONY: all

SHELL=/bin/bash -e

.DEFAULT_GOAL := help

format_all:
	poetry run ruff format .
	poetry run ruff check --fix .
	

format_changed:
	poetry run ruff format $(shell git diff --name-only | grep .py) $(shell git ls-files -o --exclude-standard | grep .py)
	poetry run ruff check --fix $(shell git diff --name-only | grep .py) $(shell git ls-files -o --exclude-standard | grep .py)


serve:
	poetry run python setup.py

run_storages:
	docker-compose -f docker-compose/storages.yaml --env-file .env up -d

down_storages:
	docker-compose -f docker-compose/storages.yaml --env-file .env down

makemigration:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic upgrade head