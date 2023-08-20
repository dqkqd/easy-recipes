import io

import pytest

from app import config
from app.file_server.image import ImageOnServer
from tests.mock_data import MockImage


@pytest.mark.usefixtures("app_context")
def test_large_image_is_cropped() -> None:
    img = MockImage.random_image(config.MAX_IMAGE_SIZE + 3, config.MAX_IMAGE_SIZE + 3)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    with ImageOnServer.from_source(image_bytes) as image_on_server:
        assert image_on_server.image.size == (
            config.MAX_IMAGE_SIZE,
            config.MAX_IMAGE_SIZE,
        )


@pytest.mark.usefixtures("app_context")
def test_small_image_is_not_cropped() -> None:
    size = 256
    assert size < config.MAX_IMAGE_SIZE

    img = MockImage.random_image(size, size)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    with ImageOnServer.from_source(image_bytes) as image_on_server:
        assert image_on_server.image.size == (size, size)


@pytest.mark.usefixtures("app_context")
def test_non_square_image_is_converted_to_square() -> None:
    img = MockImage.random_image(100, 50)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="PNG")

    with ImageOnServer.from_source(image_bytes) as image_on_server:
        assert image_on_server.image.size == (50, 50)
