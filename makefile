RUN_CONTEXT ?= docker compose exec app
TARGET ?= src
DB_USER ?= developer
DB_NAME ?= develop

up: #起動
	docker compose up -d

build: #起動 + ビルド
	docker compose up -d --build

down: #停止（コンテナ削除）
	docker compose down

destory: # コンテナ, image, volumeすべて消去 
	docker-compose down --rmi all --volumes --remove-orphans

log: # uvicornのログ確認
	docker compose logs -f app

db: # データベースとの接続
	docker compose exec db psql -U ${DB_USER} -d ${DB_NAME}

restart:	down up # コンテナの再起動

lint:	lint-mypy lint-flake8 # linterの実行

fmt:	fmt/.black fmt/.isort # formatterの実行

test: # テストの実行
	${RUN_CONTEXT} poetry run pytest tests/

migrate: # マイグレーションの実行
	${RUN_CONTEXT} poetry run alembic upgrade head
# alembic不使用時: ${RUN_CONTEXT} poetry run python src/database/migrate.py migrate

drop:	# テーブルの消去
	${RUN_CONTEXT} poetry run python src/database/migrate.py drop

shell: # appコンテナと接続
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
