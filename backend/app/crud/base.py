from contextlib import contextmanager
from typing import Generic, Iterator, Self, TypeVar

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model

from app.schemas.base import BaseSchema

ModelType = TypeVar("ModelType", bound=Model)
InDBSChemaType = TypeVar("InDBSChemaType", bound=BaseSchema)
PublicSchemaType = TypeVar("PublicSchemaType", bound=BaseSchema)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseSchema)


class CRUDBase(
    Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
        InDBSChemaType,
        PublicSchemaType,
    ],
):
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def add(self, instance: ModelType) -> None:
        self.db.session.add(instance)

    def delete(self, instance: ModelType) -> None:
        self.db.session.delete(instance)

    def commit(self) -> None:
        self.db.session.commit()

    @classmethod
    @contextmanager
    def open(cls, db: SQLAlchemy) -> Iterator[Self]:  # noqa: A003
        try:
            yield cls(db)
        except Exception:
            db.session.rollback()
            db.session.close()
            raise
