from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from flask import request
from pydantic import BaseModel, ValidationError
from werkzeug import exceptions

CREATE_INGREDIENT_PERMISSION = "create:ingredient"
DELETE_INGREDIENT_PERMISSION = "delete:ingredient"
CREATE_RECIPE_PERMISSION = "create:recipe"
DELETE_RECIPE_PERMISSION = "delete:recipe"


class Permissions(BaseModel):
    permissions: list[str]


def get_token() -> str:
    authorization = request.authorization

    if authorization is None:
        raise exceptions.Unauthorized

    if authorization.type.lower() != "bearer":  # TODO(dqk): make this as env var
        raise exceptions.Unauthorized

    token = authorization.token
    if token is None:
        raise exceptions.Unauthorized

    token = token.strip()
    if not token or len(token.split()) > 1:
        raise exceptions.Unauthorized

    return token


def check_permissions(permission: str | None, payload: dict[Any, Any]) -> None:
    try:
        allowed_permissions = Permissions(**payload)
    except ValidationError as e:
        raise exceptions.Forbidden from e

    if permission not in allowed_permissions.permissions:
        raise exceptions.Forbidden


def verify_decode_jwt(_token: str) -> dict[str, set[str]]:
    # TODO(dqk): implement this later
    return {
        "permissions": {
            CREATE_INGREDIENT_PERMISSION,
            DELETE_INGREDIENT_PERMISSION,
            CREATE_RECIPE_PERMISSION,
            DELETE_RECIPE_PERMISSION,
        },
    }


def require(permission: str | None = None) -> Callable[..., Any]:
    def requires_auth_decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            token = get_token()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
