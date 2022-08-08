"""Reused fixtures"""

import pytest
from server.app import app
from datetime import date
from server.models import (
    User,
    Rewrite,
    Source,
    Headline,
    db,
    new_user,
    new_headline,
    new_rewrite,
)


@pytest.fixture(scope="session", autouse=True)
def set_config_variables() -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///headlines_test"

    app.config["TESTING"] = True
    app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]
    app.config["WTF_CSRF_ENABLED"] = False


@pytest.fixture(scope="module", autouse=True)
def seed_database() -> None:

    db.session.rollback()
    db.drop_all()
    db.create_all()

    user = new_user(username="test_user", email="seed@seed.com", pwd="PASSWORD")
    source = Source(name="Amazing News", alignment="idealist")
    db.session.add_all([user, source])
    db.session.commit()

    headline = new_headline(
        text="A great thing happened", date=date.today(), source_id=source.id
    )
    db.session.add(headline)
    db.session.commit()

    rewrite = new_rewrite(
        text="An ok thing happened", headline=headline, user_id=user.id
    )
    db.session.add(rewrite)
    db.session.commit()
