from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model


class Base(Model):
    ...


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
