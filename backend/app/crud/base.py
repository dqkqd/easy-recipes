from contextlib import contextmanager
from typing import Generic, Iterator, Self, TypeVar

from flask import current_app, has_app_context
from flask_sqlalchemy import SQLAlchemy

from app import database
from app.schemas.base import BaseSchema

ModelType = TypeVar("ModelType", bound=database.Base)
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
    def _get_repository(cls, db: SQLAlchemy) -> Iterator[Self]:
        try:
            yield cls(db)
        except Exception:
            db.session.rollback()
            db.session.close()
            raise

    @classmethod
    @contextmanager
    def get_repository(cls, db: SQLAlchemy) -> Iterator[Self]:
        if has_app_context():
            yield from cls._get_repository(db)
        else:
            with current_app.app_context():
                yield from cls._get_repository(db)
