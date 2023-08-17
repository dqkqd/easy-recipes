from pathlib import Path

from flask.testing import FlaskClient


def test_get_default_ingredient(client: FlaskClient) -> None:
    response = client.get("/images/default/ingredient")
    assert response.status_code == 200

    default_image: Path = (
        Path(client.application.static_folder)
        / client.application.config["DEFAULT_INGREDIENT_IMAGE"]
    )

    assert default_image.read_bytes() == response.data


def test_get_default_recipe(client: FlaskClient) -> None:
    response = client.get("/images/default/recipe")
    assert response.status_code == 200

    default_image: Path = (
        Path(client.application.static_folder) / client.application.config["DEFAULT_RECIPE_IMAGE"]
    )

    assert default_image.read_bytes() == response.data
