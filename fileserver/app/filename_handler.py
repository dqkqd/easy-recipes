from __future__ import annotations

import os
import uuid
from functools import cached_property
from typing import Self

from cryptography.fernet import Fernet


class UniqueFilenameHandler:
    FERNET_MODEL = Fernet(os.environ.get("FILESERVER_FILE_ENCRYPT_KEY") or Fernet.generate_key())
    UUID_VERSION = 4

    def __init__(self, identifier: uuid.UUID | None = None) -> None:
        if identifier is None:
            self.identifier = uuid.uuid4()
        elif isinstance(identifier, uuid.UUID) and identifier.version == self.UUID_VERSION:
            self.identifier = identifier
        else:
            err_msg = f"Only UUID version {self.UUID_VERSION} is accepted."
            raise TypeError(err_msg)

    @cached_property
    def filename(self) -> str:
        return self.identifier.hex

    @cached_property
    def encrypted_filename(self) -> str:
        return self.FERNET_MODEL.encrypt(self.identifier.bytes).decode()

    @classmethod
    def from_encrypted_filename(cls, encrypted_filename: str) -> Self:
        descrypted_filename = cls.FERNET_MODEL.decrypt(encrypted_filename.encode())
        return cls(uuid.UUID(bytes=descrypted_filename, version=cls.UUID_VERSION))
