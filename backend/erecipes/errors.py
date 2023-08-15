from functools import wraps

from flask import abort, jsonify

from erecipes.models import db


def cleanup_resources(f):
    @wraps(f)
    def wrapper(*args, **kwargs) -> None:
        db.session.rollback()
        return f(*args, **kwargs)

    return wrapper


def catch_error(f):
    @wraps(f)
    def wrapper(*args, **kwargs) -> None:
        try:
            return f(*args, **kwargs)
        except ERecipesError as e:
            raise e
        except Exception as e:
            # @TODO(dqk): should log this instead print out
            print(e)
            abort(422)

    return wrapper


class ERecipesError(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def info(self):
        return {"message": self.message}


@cleanup_resources
def handle_error(e: ERecipesError):
    return jsonify(e.info()), e.status_code


@cleanup_resources
def unprocessable(_e: Exception):
    return jsonify({"message": "Unprocessable."}), 422
