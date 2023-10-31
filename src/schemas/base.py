"""スキーマ基底クラス定義"""
from datetime import datetime
from uuid import UUID

from humps import camel
from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    return camel.case(string)


class BaseRequestModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        # frozen=True,  # __init__で値の生成ができなくなる
        alias_generator=to_camel,  # 各フィールドにキャラメルケースのエイリアスを作成
        allow_population_by_field_name=True,  # キャラメルケースで送られてきたリクエストも許可する
    )


class BaseResponseModel(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        extra="forbid",  # 定義していないフィールドの無視
        frozen=True,  # フィールド値の変更を許可しない
        alias_generator=None,
        allow_population_by_field_name=False,
        from_attributes=True,  # 返却値は.model_validateで生成
    )
