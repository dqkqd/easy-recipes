import io

import pytest
import requests
from PIL import Image

from app.file_server_handler import file_server


def verify_image(url: str) -> None:
    r = requests.get(url, timeout=0.5)
    assert r.status_code == 200
    Image.open(io.BytesIO(r.content))


@pytest.mark.usefixtures("app")
def test_upload_image_from_bytes() -> None:
    img = Image.new("RGB", (256, 256))
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    identifier = file_server.add(image_bytes)
    requested_image_bytes = file_server.get(identifier)

    assert image_bytes.getvalue() == requested_image_bytes.getvalue()


@pytest.mark.skip()
@pytest.mark.usefixtures("app")
def test_upload_image_from_url() -> None:
    img = Image.new("RGB", (256, 256))
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")
    identifier = file_server._add_bytes(image_bytes)
    image_url = file_server.uri(identifier)

    new_identifier = file_server._add_url(image_url)
    requested_image_bytes = file_server.get(identifier)

    assert identifier != new_identifier
    assert image_bytes.getvalue() == requested_image_bytes.getvalue()
