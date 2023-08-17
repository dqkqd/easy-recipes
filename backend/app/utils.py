from flask import Flask


def default_ingredient_image_uri(app: Flask) -> str:
    image_uri = app.config.get("DEFAULT_INGREDIENT_IMAGE_URI")
    if not isinstance(image_uri, str):
        msg = "Default ingredient image is not set."
        raise TypeError(msg)
    return image_uri


def default_recipe_image_uri(app: Flask) -> str:
    image_uri = app.config.get("DEFAULT_RECIPE_IMAGE_URI")
    if not isinstance(image_uri, str):
        msg = "Default recipe image is not set."
        raise TypeError(msg)
    return image_uri
