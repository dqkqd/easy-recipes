import io

import requests
from PIL import Image

from app.file_server_handler import file_server


def verify_image(url: str) -> bool:
    r = requests.get(url, timeout=0.5)
    assert r.status_code == 200
    Image.open(io.BytesIO(r.content))


def test_upload_image_from_bytes() -> None:
    img = Image.new("RGB", (256, 256))
    byte_array = io.BytesIO()
    img.save(byte_array, format="PNG")
    identifier = file_server.upload_image_from_bytes(byte_array)
    image_byte = file_server.get_image(identifier)
    image = Image.open(image_byte)
    assert img == image
