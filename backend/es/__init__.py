from flask import Flask

from es.config import BaseConfig, Config


def create_app(config: type[BaseConfig] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    from es.models import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)

    return app
