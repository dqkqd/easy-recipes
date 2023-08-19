import io
from pathlib import Path

from app import config
from app.file_server import fs
from app.image.b64image import ImageHandler
from tests.mock_data import random_image


def test_add_from_bytes() -> None:
    img = random_image(config.MAX_IMAGE_SIZE, config.MAX_IMAGE_SIZE)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    image_identifier = ImageHandler.from_bytes(image_bytes).upload(fs)
    responsed_bytes = fs.get(image_identifier)

    assert image_bytes.getvalue() == responsed_bytes.getvalue()


def test_add_from_file(tmp_path: Path) -> None:
    file = tmp_path / "file.png"
    img = random_image(config.MAX_IMAGE_SIZE, config.MAX_IMAGE_SIZE)
    img.save(file, format="PNG")

    image_identifier = ImageHandler.from_file(file).upload(fs)
    responsed_bytes = fs.get(image_identifier)
    assert file.read_bytes() == responsed_bytes.getvalue()


def test_add_from_url() -> None:
    img = random_image(config.MAX_IMAGE_SIZE, config.MAX_IMAGE_SIZE)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    image_identifier = ImageHandler.from_bytes(image_bytes).upload(fs)
    image_url = fs.uri(image_identifier)

    new_image_identifier = ImageHandler.from_url(image_url).upload(fs)
    responsed_bytes = fs.get(new_image_identifier)

    assert image_identifier != new_image_identifier
    assert image_bytes.getvalue() == responsed_bytes.getvalue()
