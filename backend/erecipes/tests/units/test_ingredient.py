import json

from flask.testing import FlaskClient


def test_200_create_ingredient(client: FlaskClient) -> None:
    response = client.post(
        "/ingredients/",
        json={
            "name": "Meat",
            "image": "https://this-is-meat-example.com",
        },
    )

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["id"] == 1
