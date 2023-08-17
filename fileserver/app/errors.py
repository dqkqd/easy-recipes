import logging
from functools import wraps
from typing import Any

from flask import Response, jsonify
from werkzeug import exceptions

logger = logging.getLogger(__name__)


def to_http_error(f):  # noqa: ANN201, ANN001
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any):  # noqa: ANN401, ANN202
        try:
            return f(*args, **kwargs)
        except exceptions.HTTPException:
            raise
        except Exception as e:
            logger.exception("")
            raise exceptions.UnprocessableEntity from e

    return wrapper


def not_found(_e: exceptions.NotFound) -> Response:
    return jsonify({"message": "Resources not found."}), 404


def unprocessable(_e: exceptions.UnprocessableEntity) -> Response:
    return jsonify({"message": "Unprocessable."}), 422


def no_uploaded_image(_e: exceptions.BadRequestKeyError) -> Response:
    return jsonify({"message": "No image provided."}), 400
