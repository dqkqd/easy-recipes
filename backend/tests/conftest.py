from typing import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import auth, create_app
from app.auth import Permissions
from app.config import TestingConfig
from app.database import db


@pytest.fixture()
def app() -> Iterator[Flask]:
    app = create_app(TestingConfig)

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


@pytest.fixture(autouse=True)
def mock_auth(monkeypatch: pytest.MonkeyPatch) -> None:  # noqa: PT004
    # TODO(dqk): try to run a real test if os.environ contains token.
    def mock_return_permission(token: str) -> str:
        return Permissions(permissions=[token])

    monkeypatch.setattr(auth, "verify_decode_jwt", mock_return_permission)
