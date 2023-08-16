from __future__ import annotations

import logging
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable

from flask import current_app, jsonify
from pydantic import ValidationError

if TYPE_CHECKING:
    from werkzeug import Response

logger = logging.getLogger(__name__)


class ERecipesError(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def info(self) -> dict[str, str]:
        return {"message": self.message}

    @classmethod
    def from_validation_error(cls, e: ValidationError) -> ERecipesError:
        return ERecipesError(f"Invalid {e.errors()[0]['loc'][0]}.", 422)

    @classmethod
    def from_exception(cls, e: Exception) -> ERecipesError:
        return ERecipesError(str(e), 422)


def to_handleable_error(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return f(*args, **kwargs)
        except ERecipesError:
            raise
        except ValidationError as e:
            raise ERecipesError.from_validation_error(e) from e
        except Exception as e:  # noqa: BLE001
            raise ERecipesError.from_exception(e) from e

    return wrapper


def handle_error(e: ERecipesError) -> tuple[Response, int]:
    if current_app.debug:
        logger.exception("Exception occured.")
    return jsonify(e.info()), e.status_code
