from functools import wraps
from typing import Any

from cryptography.fernet import Fernet
from flask import current_app, request
from werkzeug import exceptions


def require_password(f):  # noqa: ANN201, ANN001
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        key = current_app.config["FILESERVER_ENCRYPT_KEY"]
        fernet_model = Fernet(key)

        try:
            token = request.headers.get("fileserver-token")
            if (
                fernet_model.decrypt(token.encode()).decode()
                != current_app.config["FILESERVER_PASSWORD"]
            ):
                raise
        except Exception as e:  # noqa: BLE001
            raise exceptions.Unauthorized from e

        return f(*args, **kwargs)

    return wrapper
