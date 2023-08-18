from __future__ import annotations

import logging
from functools import wraps
from typing import Any, Callable

from cryptography import fernet
from flask import Response, jsonify
from werkzeug import exceptions

logger = logging.getLogger(__name__)


def to_http_error(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        try:
            return f(*args, **kwargs)
        except exceptions.HTTPException:
            raise
        except (fernet.InvalidToken, ValueError) as e:
            logger.exception("")
            raise exceptions.InternalServerError from e
        except Exception as e:
            logger.exception("")
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
