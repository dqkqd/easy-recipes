from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Self

from flask import current_app, has_app_context
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, instance: Model) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, instance: Model) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def add(self, instance: Model) -> None:
        self.db.session.add(instance)

    def delete(self, instance: Model) -> None:
        self.db.session.delete(instance)

    def commit(self):
        self.db.session.commit()

    @classmethod
    def _get_repository(cls, db: SQLAlchemy) -> Self:
        try:
            yield cls(db)
        except Exception as e:
            db.session.rollback()
            db.session.close()
            raise e

    @classmethod
    @contextmanager
    def get_repository(cls, db: SQLAlchemy) -> Self:
        if has_app_context():
            yield from cls._get_repository(db)
        else:
            with current_app.app_context():
                yield from cls._get_repository(db)
