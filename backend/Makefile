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