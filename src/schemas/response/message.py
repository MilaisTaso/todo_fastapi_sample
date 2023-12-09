from pydantic import BaseModel, Field, ConfigDict


class MessageResponse(BaseModel):
    message: str = Field(min_length=1)
    
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        alias_generator=None,
        allow_population_by_field_name=False,
        from_attributes=True
    )