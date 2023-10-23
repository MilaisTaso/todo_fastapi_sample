# python3.11のイメージをダウンロード
FROM python:3.11-buster

ARG POETRY_VERSION=1.4.2

# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file/59812588
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TZ=Asia/Tokyo

WORKDIR /app
ENV PYTHONPATH=/app

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# poetryの定義ファイルをコピー
COPY pyproject.toml poetry.lock ./

# poetry初期設定
RUN poetry config virtualenvs.in-project true

# poetry.lockとpyproject.tomlの不一致があった場合、不一致を解決
RUN poetry lock

# poetry ライブラリインストール
RUN poetry install --no-root

RUN apt update -yqq && \
    apt install -y --no-install-recommends \
    build-essential curl ca-certificates \
    file git locales sudo && \
    locale-gen ja_JP.UTF-8 && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload", "--reload-exclude", "'.#*'"]