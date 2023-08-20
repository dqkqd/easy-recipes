from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from app.database import db

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseModelMixin(db.Model):  # type: ignore  # noqa: PGH003
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    name: Mapped[str]
    image_uri: Mapped[str] = mapped_column(nullable=True)


class ToSchemaModelMixin(db.Model):  # type: ignore  # noqa: PGH003
    __abstract__ = True

    def to_schema(self, schema: type[SchemaType]) -> SchemaType:
        return schema.model_validate(self)
