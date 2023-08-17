from __future__ import annotations


def validate_trailing_spaces(s: str) -> str:
    s = s.strip()
    if not s:
        msg = "Has trailing spaces"
        raise ValueError(msg)
    return s
