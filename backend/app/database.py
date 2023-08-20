from contextlib import contextmanager
from typing import Iterator

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.orm import Mapped, mapped_column


class BaseORMModel(Model):
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003


db = SQLAlchemy(model_class=BaseORMModel)
migrate = Migrate()


@contextmanager
def safe_db() -> Iterator[SQLAlchemy]:
    try:
        yield db
    except Exception:
        db.session.rollback()
        db.session.close()
        raise
