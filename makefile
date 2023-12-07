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

restart:	down up

db:
	docker compose exec db psql -U ${DB_USER} -d ${DB_NAME}

lint:	lint-mypy lint-flake8

fmt:	fmt/.black fmt/.isort

migrate:
	${RUN_CONTEXT} poetry run python src/database/migrate.py migrate

drop:	
	${RUN_CONTEXT} poetry run python src/database/migrate.py drop

shell:
	${RUN_CONTEXT} bash

# 詳細-------------------------------------
lint-mypy:
	$(RUN_CONTEXT) poetry run mypy ${TARGET}

lint-flake8:
	$(RUN_CONTEXT) poetry run flake8 ${TARGET}

fmt/.black:
	$(RUN_CONTEXT) poetry run black ${TARGET}

fmt/.isort:	
	$(RUN_CONTEXT) poetry run isort ${TARGET}
