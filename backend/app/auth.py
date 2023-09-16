from __future__ import annotations

import json
import os
from functools import wraps
from typing import Any, Callable
from urllib.request import urlopen

from flask import request
from jose import jwt
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

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = [os.environ.get("ALGORITHM")]
API_AUDIENCE = os.environ.get("API_AUDIENCE")


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


def verify_decode_jwt(token: str) -> Permissions:
    try:
        url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        with urlopen(url) as jsonurl:  # noqa: S310
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            keys = jwks.get("keys", [])

            rsa_key = {}
            try:
                for key in keys:
                    if key["kid"] != unverified_header["kid"]:
                        continue
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }
            except KeyError as e:
                raise InvalidAuthorizationTokenError from e

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )
        permissions = payload.get("permissions", [])
        return Permissions(permissions=permissions)

    except (
        jwt.JWTError,
        jwt.JWSError,
        jwt.ExpiredSignatureError,
        jwt.JWTClaimsError,
    ) as e:
        raise InvalidAuthorizationTokenError from e
    except Exception as e:  # noqa: BLE001
        raise InvalidAuthorizationTokenError from e


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
