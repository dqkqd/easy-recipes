from functools import wraps
from typing import Any, Callable

from cryptography.fernet import Fernet
from flask import current_app, request
from werkzeug import exceptions


def require_password(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        try:
            key = current_app.config["FILE_SERVER_ENCRYPT_KEY"]
            fernet_model = Fernet(key)

            authorization = request.authorization
            if authorization is None:
                raise

            if authorization.type.lower() != current_app.config["AUTHORIZATION_SCHEME"].lower():
                raise

            token = authorization.token
            if token is None:
                raise

            if (
                fernet_model.decrypt(token.encode()).decode()
                != current_app.config["FILE_SERVER_PASSWORD"]
            ):
                raise

        except Exception as e:  # noqa: BLE001
            raise exceptions.Unauthorized from e

        return f(*args, **kwargs)

    return wrapper
