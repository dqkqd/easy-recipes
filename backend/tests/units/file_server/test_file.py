import io
from pathlib import Path

import pytest
from werkzeug import exceptions

from app.file_server import fs
from app.file_server.file import FileOnServer
from tests.mocks import MockImage


@pytest.mark.usefixtures("app_context")
def test_add_from_bytes_io() -> None:
    img = MockImage.random(256, 256)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    with FileOnServer.from_source(image_bytes) as image_on_server:
        assert image_bytes.getvalue() == image_on_server.data.getvalue()


@pytest.mark.usefixtures("app_context")
def test_add_from_bytes() -> None:
    img = MockImage.random(256, 256)

    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    raw_bytes = image_bytes.getvalue()

    with FileOnServer.from_source(raw_bytes) as image_on_server:
        assert image_bytes.getvalue() == image_on_server.data.getvalue()


@pytest.mark.usefixtures("app_context")
def test_add_from_file(tmp_path: Path) -> None:
    file = tmp_path / "file.png"
    img = MockImage.random(256, 256)
    img.save(file, format="PNG")

    with FileOnServer.from_source(file) as image_on_server:
        assert file.read_bytes() == image_on_server.data.getvalue()


@pytest.mark.usefixtures("app_context")
def test_add_from_url() -> None:
    img = MockImage.random(256, 256)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    with FileOnServer.from_source(image_bytes) as image_on_server:
        identifier = image_on_server.identifier
        image_uri = image_on_server.uri
        assert image_bytes.getvalue() == image_on_server.data.getvalue()

    with FileOnServer.from_source(image_uri) as image_on_server:
        new_identifier = image_on_server.identifier
        new_image_bytes = image_on_server.data

    assert identifier != new_identifier
    assert image_bytes.getvalue() == new_image_bytes.getvalue()


@pytest.mark.usefixtures("app_context")
def test_add_from_bytes_clean_up_after_exception() -> None:
    img = MockImage.random(256, 256)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    with pytest.raises(  # noqa: PT012
        exceptions.InternalServerError,
    ), FileOnServer.from_source(
        image_bytes,
    ) as image_on_server:
        identifier = image_on_server.identifier
        raise exceptions.InternalServerError

    with pytest.raises(exceptions.NotFound):
        fs.get(identifier)
