RUN_CONTEXT ?= docker compose exec app
TARGET ?= src
DB_USER ?= postgres
DB_NAME ?= sample

up:
	docker compose up -d

build:
	docker compose up -d --build

down:
	docker compose down

log:
	docker compose logs -f app

restart: down up

db:
	docker compose exec db psql -U ${DB_USER} -d ${DB_NAME}

lint: lint/.mypy lint/.flake8

fmt: fmt/.black fmt/.isort

test: test/.pytest

migrate:
	${RUN_CONTEXT} poetry run python src/database/migrate.py

test_all: test/.pytest_all

shell:
	${RUN_CONTEXT} bash

# 詳細-------------------------------------
db/.create_table:
	$(RUN_CONTEXT) poetry run python src/db/create_master_data_table.py

lint/.mypy:
	$(RUN_CONTEXT) poetry run mypy ${TARGET}

lint/.flake8:
	$(RUN_CONTEXT) poetry run flake8 ${TARGET}

fmt/.black:
	$(RUN_CONTEXT) poetry run black ${TARGET}

fmt/.isort:
	$(RUN_CONTEXT) poetry run isort ${TARGET}

test/.pytest:
	$(RUN_CONTEXT) poetry run pytest -v ${TEST_TARGET} -k "not ${TEST_EXCLUSION}"

test/.pytest_all:
	$(RUN_CONTEXT) poetry run pytest -v ${TEST_TARGET}
