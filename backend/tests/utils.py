from __future__ import annotations

import os
from typing import TYPE_CHECKING

from app.file_server import fs

if TYPE_CHECKING:
    from pydantic_core import Url


def compare_image_data_from_uri(uri1: Url | None, uri2: Url | None) -> bool:
    if uri1 is None or uri2 is None:
        return uri1 is None and uri2 is None
    return fs.get_from_uri(uri1).getvalue() == fs.get_from_uri(uri2).getvalue()


def get_menu_manager_token() -> str | None:
    return os.environ.get("MENU_MANAGER_TOKEN")


def get_manager_token() -> str | None:
    return os.environ.get("MANAGER_TOKEN")


def should_use_real_auth_test() -> bool:
    use_real_auth_test = os.environ.get("USE_REAL_AUTH_TEST", "false").lower() in (
        "true",
        "1",
    )

    return (
        use_real_auth_test
        and get_manager_token() is not None
        and get_menu_manager_token() is not None
    )
