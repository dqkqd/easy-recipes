from __future__ import annotations

from typing import TYPE_CHECKING

from app.file_server import fs

if TYPE_CHECKING:
    from pydantic_core import Url


def compare_image_data_from_uri(uri1: Url | None, uri2: Url | None) -> bool:
    if uri1 is None or uri2 is None:
        return uri1 is None and uri2 is None
    return fs.get_from_uri(uri1).getvalue() == fs.get_from_uri(uri2).getvalue()
