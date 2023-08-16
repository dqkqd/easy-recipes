import json

import pytest
from flask.testing import FlaskClient


def test_get_recipes_no_recipes(client: FlaskClient) -> None:
    response = client.get("/recipes/")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data["recipes"]) == 0


@pytest.mark.skip()
def test_get_recipes_has_recipes(client: FlaskClient) -> None:
    raise NotImplementedError("Implement a fixture that automatically add mock data")
    raise NotImplementedError("Get recipes per pages")

    response = client.get("/recipes/")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data) > 0

    raise NotImplementedError("Make sure responsed data is equal ...")