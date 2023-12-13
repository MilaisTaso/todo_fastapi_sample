RUN_CONTEXT ?= docker compose exec app
TARGET ?= src
DB_USER ?= developer
DB_NAME ?= develop

up:
	docker compose up -d

build:
	docker compose up -d --build

down:
	docker compose down

delete:
	docker-compose down --rmi all --volumes --remove-orphans

log:
	docker compose logs -f app

db:
	docker compose exec db psql -U ${DB_USER} -d ${DB_NAME}

restart:	down up

lint:	lint-mypy lint-flake8

fmt:	fmt/.black fmt/.isort

test:
	${RUN_CONTEXT} poetry run pytest tests/

migrate: 
	${RUN_CONTEXT} poetry run alembic upgrade head
# alembic不使用時: ${RUN_CONTEXT} poetry run python src/database/migrate.py migrate

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
