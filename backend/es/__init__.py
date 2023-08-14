from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from es.models import db

    db.init_app(app)
    return app
