from cryptography.fernet import Fernet

from app.filename_handler import UniqueFilenameHandler


def test_unique_filename_handler_can_reversed() -> None:
    for _ in range(50):
        key = Fernet.generate_key().decode()
        handler = UniqueFilenameHandler(key)
        filename = handler.filename
        encrypted_filename = handler.encrypted_filename
        for _ in range(5):
            next_handler = UniqueFilenameHandler.from_encrypted_filename(key, encrypted_filename)
            encrypted_filename = next_handler.encrypted_filename
            assert filename == next_handler.filename
