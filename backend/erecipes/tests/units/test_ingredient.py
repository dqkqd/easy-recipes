import json

from flask.testing import FlaskClient


def test_create_ingredient(client: FlaskClient) -> None:
    response = client.post(
        "/clients/",
        data={
            "name": "Meal2",
            "image": "",
        },
    )

    json.loads(response.data)

    assert response.status_code == 200
    raise NotImplementedError("Do something with data")
