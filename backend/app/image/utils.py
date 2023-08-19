from __future__ import annotations

import io

from PIL import Image
from werkzeug import exceptions

from app import config


def transform_image_stream(stream: io.BytesIO | io.BufferedReader) -> io.BytesIO:
    try:
        image = Image.open(stream)
        image = crop_center(image)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
    except Exception as e:  # noqa: BLE001 #TODO(dqk): remove hard code
        raise exceptions.UnsupportedMediaType("Invalid image") from e
    else:
        return image_bytes


def crop_center(image: Image.Image) -> Image.Image:
    w, h = image.size
    crop_size = min(max(w, h), config.MAX_IMAGE_SIZE)
    return image.crop(
        (
            (w - crop_size) // 2,
            (h - crop_size) // 2,
            (w + crop_size) // 2,
            (h + crop_size) // 2,
        ),
    )
