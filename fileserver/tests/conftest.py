import shutil
from typing import TYPE_CHECKING, Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import TestingConfig

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture()
def app() -> Iterator[Flask]:
    app = create_app(TestingConfig)

    yield app

    data_folder: Path = app.config["DATA_FOLDER"]
    if data_folder.exists():
        shutil.rmtree(data_folder)


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()