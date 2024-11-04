import os
import tempfile

import pytest

from server import app, db


@pytest.fixture
def client():
    app.config.update({'TESTING': True})
    with app.test_client() as client:
        db.drop_all()
        db.create_all()
        yield client

def test_register(client):

    resp = client.post('/register', json = {"email":"a", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
