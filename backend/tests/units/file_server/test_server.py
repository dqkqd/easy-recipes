import io

import pytest
from werkzeug import exceptions

from app.file_server import fs
from tests.mocks import MockImage


@pytest.mark.usefixtures("app_context")
def test_add_file_from_bytes() -> None:
    img = MockImage.random(256, 256)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    identifier = fs.add(image_bytes)
    requested_image_bytes = fs.get(identifier)

    assert image_bytes.getvalue() == requested_image_bytes.getvalue()


@pytest.mark.usefixtures("app_context")
def test_add_file_from_url() -> None:
    img = MockImage.random(256, 256)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    identifier = fs.add(image_bytes)
    image_uri = fs.file_uri(identifier)

    new_identifier = fs.add(image_uri)
    requested_image_bytes = fs.get(new_identifier)

    assert identifier != new_identifier
    assert image_bytes.getvalue() == requested_image_bytes.getvalue()


@pytest.mark.usefixtures("app_context")
def test_delete_file() -> None:
    img = MockImage.random(256, 256)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")
    identifier = fs.add(image_bytes)

    fs.delete(identifier)
    with pytest.raises(exceptions.NotFound):
        fs.get(identifier)
