# FastAPI 学習用テンプレート

FastAPIを使用した学習やちょっとしたアプリの作成に使用可能なテンプレートとして作成しました。

## 実行環境

* python 3.11+
* poetry
* docker


## 使用方法

.env.example を.env にリネームしてください。
必要に応じて環境変数を変更して下さい。
SECRET_KEYはpoetryでライブラリをインストールした後、opensslで生成すると楽です。

下記コマンドにて環境構築が可能です。

```bash
make up
```

下記コマンドでマイグレーションの実行ができます。

```bash
make migrate
```

下記URLでSwagger UIにアクセスできます。

```
ttp://localhost:8000/docs
```

開発時にコード補完を有効にしたい場合は、ローカル環境にpython, poetryをインストールし、
`poetry install`にてローカルの仮想環境にもライブラリをインストールして下さい。
VS Codeの場合はpylanceがあれば、コード補完が有効になるはずです。

その他使用方法についてはmakefileを確認してください


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
repository/base.py に データベース操作の共通のクラスを実装していますので、
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

### リクエスト・レスポンスにキャメルケースのエイリアスを追加

pythonではスネークケースでの定義基本ですが、フロントエンドによってはキャメルケースが標準なため、
キャメルケースのリクエストを許可およびレスポンス応答のため、pydanticにキャメルケースのエイリアスを作成しています。

リクエスト・レスポンスの型を定義する際は schemas/base.pyを継承して作成してください。


### Settings

core/config.py にて、pydanticのBaseSettings を継承してアプリ共有の設定をしています。
.envファイルから自動的に設定を読み込むことができる他、状況に応じて.envファイルの切り替えが可能です。


### 例外処理

表示用の例外はAPIExceptionクラスをしようします。
引数にErrorMessageクラスを渡すことで、クラス名をエラー識別子、定義したテキストを表示できます。
エラー定義の追加はErrorMessageクラス内に実装してください。

### ログ出力

docker起動時にログ設定ファイルを読み込みuvicornを起動しています。
ログの設定を変える際は logger/logger_config.yamlを修正してください


### テスト

tests/ ディレクトリ配下がテスト関連のファイルです。
テストの実行は`make test`で行います。テスト対象はsrc/ ディレクトリ配下です。

conftest.py にてテスト実行前に下記の処理を行っています。

* テスト用データベースの作成（pytest-postgres）
* データベースとのセッションの作成
* マイグレーションの実行
* 認証情報を付与した非同期テストクライアントの作成

その他処理を追加する際はpytest.fixtureを使用して定義してください。
また、conftest.py はテスト実行前に自動で処理を行いますが、処理内容はテストファイルの階層かそれ以上の階層にあるものが有効な処理になりますので、適切な場所へ処理を追加してください。


### その他機能

* alembicを使用した非同期マイグレーション（`make migrate`で実行）
* linter(mypy, flake8)の使用
* formatter(black, isort)の使用
