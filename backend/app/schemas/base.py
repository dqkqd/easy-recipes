from __future__ import annotations

from pydantic import (
    BaseModel,
)


class BaseSchema(BaseModel):
    pass


class IDModelMixin(BaseSchema):
    id: int  # noqa: A003
