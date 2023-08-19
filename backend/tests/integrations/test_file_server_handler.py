import io

import pytest
from PIL import Image
from werkzeug import exceptions

from app.file_server import fs


@pytest.mark.usefixtures("app_context")
def test_add_file_from_bytes() -> None:
    img = Image.new("RGB", (256, 256))
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    identifier = fs.add(image_bytes)
    requested_image_bytes = fs.get(identifier)

    assert image_bytes.getvalue() == requested_image_bytes.getvalue()


@pytest.mark.usefixtures("app_context")
def test_add_file_from_url() -> None:
    img = Image.new("RGB", (256, 256))
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")
    identifier = fs.add(image_bytes)
    image_url = fs.uri(identifier)

    new_identifier = fs.add(image_url)
    requested_image_bytes = fs.get(identifier)

    assert identifier != new_identifier
    assert image_bytes.getvalue() == requested_image_bytes.getvalue()


@pytest.mark.usefixtures("app_context")
def test_delete_file() -> None:
    img = Image.new("RGB", (256, 256))
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")
    identifier = fs.add(image_bytes)

    fs.delete(identifier)
    with pytest.raises(exceptions.NotFound):
        fs.get(identifier)
