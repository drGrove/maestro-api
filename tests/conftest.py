# tests/conftest.py
import pytest
from maestro_api import create_app, db

@pytest.fixture(scope="session")
def app(request):
    print("App Setup")
    app = create_app()
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        print("app teardown")
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="session")
def client(request, app):
    client = app.test_client()
    return client
