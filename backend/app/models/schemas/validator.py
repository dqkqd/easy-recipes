from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from app.errors import ERecipesError

if TYPE_CHECKING:
    from pydantic_core import Url


def validate_trailing_spaces(s: str) -> str:
    s = s.strip()
    if not s:
        msg = "Has trailing spaces"
        raise ValueError(msg)
    return s


def validate_url_exists(url: Url, err_msg: str | None = None) -> Url:
    try:
        r = requests.head(url, timeout=10)
        if r.status_code != 200:
            raise
    except Exception as e:  # noqa: BLE001
        if err_msg is None:
            err_msg = "Provided url does not exist."
        raise ERecipesError(err_msg, 422) from e

    return url
