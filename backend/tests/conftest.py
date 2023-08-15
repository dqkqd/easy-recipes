import os
from typing import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from erecipes import create_app
from erecipes.config import TestingConfig
from erecipes.models import db


@pytest.fixture()
def app() -> Iterator[Flask]:
    app = create_app(TestingConfig)

    test_db_path = app.config.get("TEST_DB_PATH")
    assert test_db_path is not None
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def app_context(app: Flask) -> Iterator[None]:  # noqa: PT004
    """https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/contexts/#tests"""
    with app.app_context():
        yield
