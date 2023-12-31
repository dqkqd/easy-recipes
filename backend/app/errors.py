from __future__ import annotations

import logging
from functools import wraps
from typing import Any, Callable, Self

from flask import current_app, jsonify
from pydantic import ValidationError
from werkzeug import Response, exceptions

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
        except exceptions.NotFound as e:
            e.description = "Resources not found."
            raise ApplicationHTTPError.from_http_error(e) from e
        except exceptions.Unauthorized as e:
            e.description = "Unauthorized."
            raise ApplicationHTTPError.from_http_error(e) from e
        except exceptions.Forbidden as e:
            e.description = "Forbidden."
            raise ApplicationHTTPError.from_http_error(e) from e
        except exceptions.HTTPException as e:
            raise ApplicationHTTPError.from_http_error(e) from e
        except ValidationError as e:
            raise ApplicationHTTPError.from_pydantic_validation_error(e) from e

    return wrapper


class BaseError(exceptions.HTTPException):
    def __init__(
        self,
        code: int | None = None,
        description: str | None = None,
        response: Response | None = None,
    ) -> None:
        if code is not None:
            self.code = code
        super().__init__(description, response)

    def info(self) -> dict[str, str | int]:
        if not isinstance(self.code, int) or not isinstance(self.description, str):
            raise NotImplementedError(self)
        return {"code": self.code, "message": self.description}


class ApplicationHTTPError(BaseError):
    code: int = 422
    description: str = "Unprocessable."

    @classmethod
    def from_http_error(cls, e: exceptions.HTTPException) -> Self:
        response = e.get_response()
        if not isinstance(response, Response):
            raise TypeError(response)
        return cls(code=e.code, description=e.description, response=response)

    @classmethod
    def from_pydantic_validation_error(cls, e: ValidationError) -> Self:
        field = e.errors()[0]["loc"][0]
        return cls(code=422, description=f"Invalid {field}.")


class ServerAlreadyInitializedError(exceptions.InternalServerError):
    ...


class ServerConfigError(exceptions.InternalServerError):
    ...


class ServerDeleteWrongFileError(exceptions.InternalServerError):
    ...


class NoAuthorizationHeaderError(exceptions.Unauthorized):
    ...


class InvalidAuthorizationTypeError(exceptions.Unauthorized):
    ...


class InvalidAuthorizationTokenError(exceptions.Unauthorized):
    ...


class InvalidPermissionError(exceptions.Forbidden):
    ...
