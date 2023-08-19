from __future__ import annotations

import io
from contextlib import contextmanager, suppress
from functools import cached_property, singledispatchmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator, Self

import requests
from pydantic_core import Url
from werkzeug import exceptions

from app.file_server import fs

if TYPE_CHECKING:
    from app.file_server.server import FileIdentifer


class FileOnServer:
    def __init__(self, _identifier: FileIdentifer) -> None:
        self._identifier = _identifier

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def uri(self) -> Url:
        return fs.file_uri(self.identifier)

    @cached_property
    def data(self) -> io.BytesIO:
        return fs.get(self.identifier)

    @singledispatchmethod
    @classmethod
    def validator(cls, source: Any) -> Any:  # https://github.com/python/typeshed/issues/5560
        raise NotImplementedError(type(source))

    @classmethod
    @contextmanager
    def from_source(cls, source: Any) -> Iterator[Self]:
        try:
            file_on_server = cls._from_source(source)
            yield file_on_server
        except NotImplementedError:
            raise
        except Exception:
            fs.delete(file_on_server.identifier)
            raise

    @singledispatchmethod
    @classmethod
    def _from_source(cls, source: Any) -> Self:
        raise NotImplementedError(type(source))

    @_from_source.register
    @classmethod
    def _(cls, stream: io.BytesIO | io.BufferedReader) -> Self:
        with suppress(NotImplementedError):
            stream = cls.validator(stream)
        identifier = fs.add(stream)
        return cls(identifier)

    @_from_source.register(Path)
    @classmethod
    def _(cls, file: Path) -> Self:
        with suppress(NotImplementedError):
            file = cls.validator(file)
        return cls._from_source(file.open("rb"))

    @_from_source.register(Url)
    @classmethod
    def _(cls, url: Url) -> Self:
        with suppress(NotImplementedError):
            url = cls.validator(url)
        r = requests.get(str(url), timeout=fs.timeout)
        if r.status_code != 200:
            exceptions.abort(r.status_code)
        return cls._from_source(io.BytesIO(r.content))
