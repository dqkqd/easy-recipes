from app.models import db


def cleanup_resources() -> None:
    db.session.rollback()
