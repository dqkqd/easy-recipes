from __future__ import annotations

import logging
from functools import wraps
from typing import Any, Callable

from flask import Response, current_app, jsonify
from werkzeug import exceptions

from app.filename_handler import InvalidKeyError, InvalidKeyOrFileNameError

logger = logging.getLogger(__name__)


def write_exception_log() -> None:
    if current_app.debug:
        logger.exception("")


def to_http_error(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        try:
            return f(*args, **kwargs)
        except exceptions.HTTPException:
            write_exception_log()
            raise
        except InvalidKeyError as e:
            write_exception_log()
            raise exceptions.InternalServerError from e
        except InvalidKeyOrFileNameError as e:
            write_exception_log()
            raise exceptions.NotFound from e
        except Exception as e:  # noqa: BLE001
            write_exception_log()
            raise exceptions.UnprocessableEntity from e

    return wrapper


def not_found(_e: exceptions.NotFound) -> tuple[Response, int]:
    return jsonify({"message": "File not found."}), 404


def unprocessable(_e: exceptions.UnprocessableEntity) -> tuple[Response, int]:
    return jsonify({"message": "Unprocessable."}), 422


def no_uploaded_file(_e: exceptions.BadRequestKeyError) -> tuple[Response, int]:
    return jsonify({"message": "No file provided."}), 400


def file_too_large(_e: exceptions.RequestEntityTooLarge) -> tuple[Response, int]:
    return jsonify({"message": "File too large."}), 413


def inernal_server_error(_e: exceptions.InternalServerError) -> tuple[Response, int]:
    return jsonify({"message": "Internal Server Error."}), 500


def unauthorized(_e: exceptions.InternalServerError) -> tuple[Response, int]:
    return jsonify({"message": "Unauthorized."}), 401
