from __future__ import annotations

from typing import Generic, TypeVar

from flask_sqlalchemy.model import Model

from app.database import safe_db
from app.schemas.base import BaseSchema

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseSchema)


class CRUDBase(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType],
):
    def __init__(
        self,
        model: type[ModelType],
    ) -> None:
        self.model = model

    def get(self, id: int) -> ModelType:  # noqa: A002
        with safe_db():
            return self.model.query.filter_by(  # type: ignore  # noqa: PGH003
                id=id,
            ).one_or_404()

    def add(self, obj_create: CreateSchemaType) -> ModelType:
        with safe_db() as db:
            obj = self.model(**obj_create.model_dump())
            db.session.add(obj)
            db.session.commit()
            return obj

    def delete(self, id: int) -> ModelType:  # noqa: A002
        with safe_db() as db:
            obj = self.model.query.filter_by(id=id).one_or_404()
            db.session.delete(obj)
            db.session.commit()
            return obj  # type: ignore  # noqa: PGH003
