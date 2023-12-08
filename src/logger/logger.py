import os
from logging import Logger, getLogger
from logging.config import dictConfig

import yaml

#ログの設定 uvicornで読み込んでいるのでFastAPI上での読み込みは不要
def init_logger(filepath: str) -> None:
    with open(filepath) as f:
        config = yaml.safe_load(f)
        dictConfig(config)

#loggerの設定はこちらを使う
def get_logger(name: str) -> Logger:
    return getLogger(name)
