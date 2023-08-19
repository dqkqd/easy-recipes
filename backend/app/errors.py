from __future__ import annotations

import logging
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Self

from flask import current_app, jsonify
from werkzeug import exceptions

if TYPE_CHECKING:
    from werkzeug import Response

logger = logging.getLogger(__name__)


def handle_error(e: ApplicationHTTPError) -> tuple[Response, int]:
    if current_app.debug:
        logger.exception("Exception occured.")
    return jsonify(e.info()), e.code


def to_handleable_error(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return f(*args, **kwargs)
        except exceptions.HTTPException as e:
            raise ApplicationHTTPError.from_http_error(e) from e

    return wrapper


class BaseError(exceptions.HTTPException):
    def info(self) -> dict[str, str]:
        return {"code": self.code, "message": self.description}


class ApplicationHTTPError(BaseError):
    code = 422
    description = "Unprocessable."

    @classmethod
    def from_http_error(cls, e: exceptions.HTTPException) -> Self:
        return cls(e.description, e.response)


class ServerAlreadyInitializedError(exceptions.InternalServerError):
    ...


class ServerConfigError(exceptions.InternalServerError):
    ...


class ServerDeleteWrongFileError(exceptions.InternalServerError):
    ...
