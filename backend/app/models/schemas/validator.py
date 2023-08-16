def validate_trailing_spaces(s: str) -> str:
    s = s.strip()
    if not s:
        raise ValueError("Has trailing spaces")
    return s
