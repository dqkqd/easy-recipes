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

    identifier = file_server.upload_image_from_bytes(image_bytes)
    requested_image_bytes = file_server.get_image(identifier)

    assert image_bytes.getvalue() == requested_image_bytes.getvalue()
