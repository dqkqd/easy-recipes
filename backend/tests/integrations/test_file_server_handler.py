import io

import pytest
from PIL import Image

from app.file_server_handler import file_server


@pytest.mark.usefixtures("app")
def test_add_file_from_bytes() -> None:
    img = Image.new("RGB", (256, 256))
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    identifier = file_server.add(image_bytes)
    requested_image_bytes = file_server.get(identifier)

    assert image_bytes.getvalue() == requested_image_bytes.getvalue()


@pytest.mark.usefixtures("app")
def test_add_file_from_url() -> None:
    img = Image.new("RGB", (256, 256))
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")
    identifier = file_server.add(image_bytes)
    image_url = file_server.uri(identifier)

    new_identifier = file_server.add(image_url)
    requested_image_bytes = file_server.get(identifier)

    assert identifier != new_identifier
    assert image_bytes.getvalue() == requested_image_bytes.getvalue()
