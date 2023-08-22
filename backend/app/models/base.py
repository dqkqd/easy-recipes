from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from app.database import db

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseModelMixin(db.Model):  # type: ignore  # noqa: PGH003
    __abstract__ = True
