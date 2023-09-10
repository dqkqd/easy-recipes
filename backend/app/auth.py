from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from flask import request
from pydantic import BaseModel

from app.errors import (
    InvalidAuthorizationTokenError,
    InvalidAuthorizationTypeError,
    InvalidPermissionError,
    NoAuthorizationHeaderError,
)

CREATE_INGREDIENT_PERMISSION = "create:ingredient"
UPDATE_INGREDIENT_PERMISSION = "update:ingredient"
DELETE_INGREDIENT_PERMISSION = "delete:ingredient"
CREATE_RECIPE_PERMISSION = "create:recipe"
UPDATE_RECIPE_PERMISSION = "update:recipe"
DELETE_RECIPE_PERMISSION = "delete:recipe"


class Permissions(BaseModel):
    permissions: list[str]


def get_token() -> str:
    authorization = request.authorization
    if authorization is None:
        raise NoAuthorizationHeaderError
    if authorization.type.lower() != "bearer":
        raise InvalidAuthorizationTypeError
    if not isinstance(authorization.token, str) or not authorization.token.strip():
        raise InvalidAuthorizationTokenError
    return authorization.token


def check_permissions(permission: str | None, allowed_permissions: Permissions) -> None:
    if permission not in allowed_permissions.permissions:
        raise InvalidPermissionError


def verify_decode_jwt(_token: str) -> Permissions:
    # TODO(dqk): parse token, it should raise InvalidAuthorizationTokenError on any error
    return Permissions(
        permissions=[
            CREATE_INGREDIENT_PERMISSION,
            UPDATE_INGREDIENT_PERMISSION,
            DELETE_INGREDIENT_PERMISSION,
            CREATE_RECIPE_PERMISSION,
            UPDATE_RECIPE_PERMISSION,
            DELETE_RECIPE_PERMISSION,
        ],
    )


def require(permission: str | None = None) -> Callable[..., Any]:
    def requires_auth_decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            token = get_token()
            permissions = verify_decode_jwt(token)
            check_permissions(permission, permissions)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
