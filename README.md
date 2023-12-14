# FastAPI 学習用テンプレート

FastAPIを使用した学習やちょっとしたアプリの作成に使用可能なテンプレートとして作成しました。

## 実行環境

- python 3.11+
- poetry
- docker

## ディレクトリ構造

```text
.
|-- Dockerfile
|-- README.md
|-- alembic.ini
|-- docker-compose.yaml
|-- makefile
|-- migrations
|   |-- README
|   |-- env.py
|   |-- script.py.mako
|   `-- versions
|       |-- 2023_12_11_1035-7e9f51627c3c_initial_empty.py
|       `-- 2023_12_12_1504-226a00e19a26_create_tables.py
|-- mypy.ini
|-- poetry.lock
|-- pyproject.toml
|-- src
|   |-- __init__.py
|   |-- api               // エンドポイントの定義
|   |   |-- __init__.py
|   |   `-- v1
|   |       |-- __init__.py
|   |       |-- auth.py
|   |       |-- todos.py
|   |       `-- users.py
|   |-- core              // プロジェクト固有の設定・共通処理等
|   |   |-- config.py
|   |   `-- lib
|   |       `-- auth.py
|   |-- database         // データベース操作に関する定義・設定
|   |   |-- __init__.py
|   |   |-- migrate.py
|   |   |-- models       // ORMモデルの定義
|   |   |   |-- __init__.py
|   |   |   |-- base.py
|   |   |   |-- todos.py
|   |   |   `-- users.py
|   |   `-- setting.py
|   |-- errors          // エラーの定義
|   |   |-- __init__.py
|   |   |-- exception.py
|   |   `-- messages.py
|   |-- logger          // ログの設定
|   |   |-- __init__.py
|   |   |-- logger.py
|   |   `-- logger_config.yaml
|   |-- main.py
|   |-- repository      // データベースを操作するクラス
|   |   |-- __init__.py
|   |   |-- base.py
|   |   |-- crud
|   |   |   |-- todo.py
|   |   |   `-- user.py
|   |   `-- dependencies.py
|   `-- schemas         // リクエスト・レスポンスの型定義
|       |-- __init__.py
|       |-- base.py
|       |-- requests
|       |   |-- __init__.py
|       |   |-- todo.py
|       |   `-- user.py
|       `-- response
|           |-- __init__.py
|           |-- message.py
|           |-- todo.py
|           |-- token.py
|           `-- user.py
`-- tests              // テスト関連
    |-- __init__.py
    |-- api
    |   |-- test_root.py
    |   `-- todos
    |       |-- __init__.py
    |       |-- conftest.py
    |       `-- test_todos.py
    `-- conftest.py
```

## 大まかな機能

### DBレコードの作成・取得・更新・削除(CRUD)

SQLAlchemyのv2をベースに実装しています。<br>
repository/base.py に データベース操作の共通のクラスを実装していますので、<br>
データベース操作を行うクラスは、此方を継承して個別に処理を追加してください。


### ユーザー認証と権限(Scopes)

ユーザー認証が必要なエンドポイントには下記のように依存関係を注入します。<br>
また特定の権限を持つユーザーのみアクセスできるようにするには、scopesに適切な値を設定します。

```python
@router.get(
    "/{id}",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    status_code=status.HTTP_200_OK
)
```