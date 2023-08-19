from __future__ import annotations

from flask import Flask

from app.config import BaseConfig, Config


def create_app(config_cls: type[BaseConfig] = Config) -> Flask:
    app = Flask(__name__)

    config = config_cls()
    app.config.from_object(config)

    from app.models.database import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)

    from app.file_server import fs

    fs.init_app(app)

    from app.routes import ingredient, recipe

    app.register_blueprint(recipe.api)
    app.register_blueprint(ingredient.api)

    from app.errors import ERecipesError, handle_error

    app.register_error_handler(ERecipesError, handle_error)

    return app
