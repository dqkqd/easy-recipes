import io
from pathlib import Path

import pytest
from werkzeug import exceptions

from app import config
from app.file_server import fs
from app.image.b64image import ImageOnServer
from tests.mock_data import random_image


def test_add_from_bytes() -> None:
    img = random_image(config.MAX_IMAGE_SIZE, config.MAX_IMAGE_SIZE)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    with ImageOnServer.from_bytes(image_bytes) as image_on_server:
        assert image_bytes.getvalue() == image_on_server.byte_data.getvalue()


def test_add_from_file(tmp_path: Path) -> None:
    file = tmp_path / "file.png"
    img = random_image(config.MAX_IMAGE_SIZE, config.MAX_IMAGE_SIZE)
    img.save(file, format="PNG")

    with ImageOnServer.from_file(file) as image_on_server:
        assert file.read_bytes() == image_on_server.byte_data.getvalue()


def test_add_from_url() -> None:
    img = random_image(config.MAX_IMAGE_SIZE, config.MAX_IMAGE_SIZE)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    with ImageOnServer.from_bytes(image_bytes) as image_on_server:
        identifier = image_on_server.identifier
        image_url = image_on_server.as_uri()
        assert image_bytes.getvalue() == image_on_server.byte_data.getvalue()

    with ImageOnServer.from_url(image_url) as image_on_server:
        new_identifier = image_on_server.identifier
        new_image_bytes = image_on_server.byte_data

    assert identifier != new_identifier
    assert image_bytes.getvalue() == new_image_bytes.getvalue()


def test_add_from_bytes_clean_up_after_exception() -> None:
    img = random_image(config.MAX_IMAGE_SIZE, config.MAX_IMAGE_SIZE)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    with pytest.raises(AssertionError), ImageOnServer.from_bytes(  # noqa: PT012
        image_bytes,
    ) as image_on_server:
        identifier = image_on_server.identifier
        raise AssertionError

    with pytest.raises(exceptions.NotFound):
        fs.get(identifier)
