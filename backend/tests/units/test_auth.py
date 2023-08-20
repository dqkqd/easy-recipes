from flask.testing import FlaskClient
from pytest_mock import MockerFixture

from app import auth
from tests.mocks import MockAuth, MockIngredient


def test_200_create_ingredient_basic(mocker: MockerFixture, client: FlaskClient) -> None:
    token = auth.CREATE_INGREDIENT_PERMISSION

    mocker.patch(
        "app.auth.verify_decode_jwt",
        return_value={"permissions": [token]},
    )
    response = client.post(
        "/ingredients/",
        headers=MockAuth.authorization_header(token),
        json=MockIngredient.random_valid_ingredient_data(),
    )
    assert response.status_code == 200
