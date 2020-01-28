import os

import pytest

from maestro_api import create_app, db

@pytest.fixture(scope='module')
def app():
    app = create_app()
    db.init_app(app)
    with app.app_context():
        db.create_all()
    yield app
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    client = app.test_client()
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    yield client
