from functools import wraps
from typing import Any, Callable

from flask import jsonify
from pydantic import ValidationError
from werkzeug import Response

from app.models import db


class ERecipesError(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def info(self) -> dict[str, str]:
        return {"message": self.message}

    @classmethod
    def from_validation_error(cls, e: ValidationError) -> "ERecipesError":
        return ERecipesError(f"Invalid {e.errors()[0]['loc'][0]}.", 422)

    @classmethod
    def from_exception(cls, e: Exception) -> "ERecipesError":
        return ERecipesError(str(e), 422)


def cleanup_resources(
    f: Callable[[ERecipesError], tuple[Response, int]]
) -> Callable[[Exception], tuple[Response, int]]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> tuple[Response, int]:
        db.session.rollback()
        return f(*args, **kwargs)

    return wrapper


def catch_error(f: Callable[[], Any]) -> Callable[[], Any]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return f(*args, **kwargs)
        except ERecipesError as e:
            raise e
        except ValidationError as e:
            raise ERecipesError.from_validation_error(e) from e
        except Exception as e:
            raise ERecipesError.from_exception(e) from e

    return wrapper


@cleanup_resources
def handle_error(e: ERecipesError) -> tuple[Response, int]:
    return jsonify(e.info()), e.status_code
