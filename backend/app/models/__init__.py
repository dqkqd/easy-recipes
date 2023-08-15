from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model


class Base(Model):
    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
