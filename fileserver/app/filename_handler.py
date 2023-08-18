from __future__ import annotations

import uuid
from functools import cached_property
from pathlib import Path
from typing import Self

from cryptography.fernet import Fernet
from werkzeug import exceptions
from werkzeug.utils import secure_filename


class FilenameHandlerError(Exception):
    pass


class InvalidKeyError(FilenameHandlerError):
    pass


class InvalidKeyOrFileNameError(FilenameHandlerError):
    pass


def secure_splitext(filename: str) -> tuple[str, str]:
    try:
        file = Path(secure_filename(filename))
        ext = file.suffix.lower()
    except Exception as e:  # noqa: BLE001
        raise exceptions.UnsupportedMediaType from e

    return file.stem, ext


class UniqueFilenameHandler:
    UUID_VERSION = 4

    def __init__(self, key: str, ext: str, unique_identifier: str | None = None) -> None:
        self.ext = ext

        if unique_identifier is None:
            self.identifier = uuid.uuid4().hex
        else:
            self.identifier = unique_identifier

        try:
            self.fernet_model = Fernet(key)
        except ValueError as e:
            raise InvalidKeyError from e

    @cached_property
    def filename(self) -> str:
        return f"{self.identifier}{self.ext}"

    @cached_property
    def encrypted_filename(self) -> str:
        return self.fernet_model.encrypt(self.filename.encode()).decode()

    @classmethod
    def from_encrypted_filename(cls, key: str, encrypted_filename: str) -> Self:
        try:
            fernet_model = Fernet(key)
        except ValueError as e:
            raise InvalidKeyError from e

        try:
            descrypted_filename = fernet_model.decrypt(encrypted_filename.encode())
            name, ext = secure_splitext(descrypted_filename.decode())
            return cls(key, ext, name)
        except Exception as e:  # noqa: BLE001
            raise InvalidKeyOrFileNameError from e
