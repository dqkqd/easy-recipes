import json

import pytest
from flask.testing import FlaskClient


def test_200_create_basic(client: FlaskClient) -> None:
    response = client.post(
        "/ingredients/",
        json={
            "name": "eggs",
            "image": "https://valid-egg-url.com",
        },
    )

    data = json.loads(response.data)
    assert response.status_code == 200

    assert data == {"id": 1}


def test_200_create_duplicated_name(client: FlaskClient) -> None:
    raise NotImplementedError


def test_200_create_use_default_image_url(client: FlaskClient) -> None:
    raise NotImplementedError


def test_200_create_uploaded_image_url(client: FlaskClient) -> None:
    raise NotImplementedError("save user uploaded image")


def test_200_create_crop_user_uploaded_image(client: FlaskClient) -> None:
    raise NotImplementedError


@pytest.mark.parametrize(
    ("name", "image", "error_message"),
    [
        # invalid name
        (None, None, "Invalid name."),
        (None, "https://valid-ingredient-url.com", "Invalid name."),
        (None, "https://invalid-ingredient-url", "Invalid name."),
        ("", "https://valid-ingredient-url.com", "Invalid name."),
        (" ", "https://valid-ingredient-url.com", "Invalid name."),
        # invalid url
        # @TODO(dqk): handle empty url by using default image
        ("egg", "https://invalid-ingredient-url", "Invalid image."),
        ("egg", " ", "Invalid image."),
    ],
)
def test_422_create_invalid_name_or_url(
    client: FlaskClient, name: str | None, image: str | None, error_message: str
) -> None:
    payload = {}
    if name is not None:
        payload["name"] = name
    if image is not None:
        payload["image"] = image

    response = client.post("/ingredients/", json=payload)

    data = json.loads(response.data)

    assert response.status_code == 422
    assert data == {"message": error_message}


def test_422_create_invalid_image(client: FlaskClient) -> None:
    raise NotImplementedError("valid url but invalid image")


@pytest.mark.skip()
def test_401_create_unauthorize(client: FlaskClient) -> None:
    raise NotImplementedError


@pytest.mark.skip()
def test_403_create_no_permission(client: FlaskClient) -> None:
    raise NotImplementedError
