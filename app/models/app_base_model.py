from abc import ABC
from typing import Any
from datetime import datetime
from pydantic import BaseModel, field_validator, field_serializer, ConfigDict

from utils.strings import snake_to_camel


class AppBaseModel(ABC, BaseModel):
    """
    The most common abstract model inherited from the pydantic base model.
    It defines custom serialization rules throughout this project
    """

    model_config = ConfigDict(
        alias_generator=snake_to_camel,
        populate_by_name=True,
        validate_by_name=True,
    )

    @field_validator("*", mode="before")
    @classmethod
    def round_floats(cls, value: Any) -> Any:
        if isinstance(value, float):
            return round(value, 2)
        return value

    @field_serializer("*")
    def serialize_values(self, value: Any, info) -> Any:
        # Serialize datetime to ISO format string
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%SZ")
        # Round floats to 2 decimal places
        if isinstance(value, float):
            return round(value, 2)
        return value
