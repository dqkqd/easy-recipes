from contextlib import contextmanager
from typing import Iterator

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model


class Base(Model):
    ...


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


@contextmanager
def safe_db() -> Iterator[SQLAlchemy]:
    try:
        yield db
    except Exception:
        db.session.rollback()
        db.session.close()
        raise
