from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        alias_generator=None,
        allow_population_by_field_name=False,
    )


class TokenPayload(BaseModel):
    sub: UUID

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        alias_generator=None,
        allow_population_by_field_name=False,
        from_attributes=True,
    )
