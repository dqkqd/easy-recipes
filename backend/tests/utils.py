from pydantic_core import Url

from app.file_server import fs


def compare_image_data_from_uri(uri1: Url, uri2: Url) -> bool:
    return fs.get_from_uri(uri1).getvalue() == fs.get_from_uri(uri2).getvalue()
