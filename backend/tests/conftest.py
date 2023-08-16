from pathlib import Path
from typing import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import TestingConfig
from app.models.database import db


@pytest.fixture()
def app() -> Iterator[Flask]:
    app = create_app(TestingConfig)

    test_db_path_str = app.config.get("TEST_DB_PATH")
    assert isinstance(test_db_path_str, str)

    test_db_path = Path(test_db_path_str)
    if test_db_path.exists():
        test_db_path.unlink()

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
