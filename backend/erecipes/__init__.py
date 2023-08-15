from flask import Flask

from erecipes.config import BaseConfig, Config


def create_app(config: type[BaseConfig] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    from erecipes.models import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)

    from erecipes.routes import ingredient, recipe

    app.register_blueprint(recipe.api)
    app.register_blueprint(ingredient.api)

    return app
