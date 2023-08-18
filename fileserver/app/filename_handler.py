from __future__ import annotations

import uuid
from functools import cached_property
from typing import Self

from cryptography.fernet import Fernet


class UniqueFilenameHandler:
    UUID_VERSION = 4

    def __init__(self, key: str, identifier: uuid.UUID | None = None) -> None:
        if identifier is None:
            self.identifier = uuid.uuid4()
        elif isinstance(identifier, uuid.UUID) and identifier.version == self.UUID_VERSION:
            self.identifier = identifier
        else:
            err_msg = f"Only UUID version {self.UUID_VERSION} is accepted."
            raise TypeError(err_msg)
        self.key = key

    @cached_property
    def filename(self) -> str:
        return self.identifier.hex

    @cached_property
    def encrypted_filename(self) -> str:
        fernet_model = Fernet(self.key)
        return fernet_model.encrypt(self.identifier.bytes).decode()

    @classmethod
    def from_encrypted_filename(cls, key: str, encrypted_filename: str) -> Self:
        fernet_model = Fernet(key)
        descrypted_filename = fernet_model.decrypt(encrypted_filename.encode())
        return cls(key, uuid.UUID(bytes=descrypted_filename, version=cls.UUID_VERSION))
