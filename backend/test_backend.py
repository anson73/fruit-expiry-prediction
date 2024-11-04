import os
import tempfile

import pytest

from server import app, set_database_uri, create_db


@pytest.fixture
def client():
    os.remove("instance/test.db")
    app.config.update({'TESTING': True})
    set_database_uri('sqlite:///test.db')
    create_db()
    with app.test_client() as client:
        yield client

def test_register(client):

    resp = client.post('/register', json = {"email":"a", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
