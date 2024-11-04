import pytest
import json
from server import app, db


@pytest.fixture
def client():
    app.config.update({'TESTING': True})
    with app.test_client() as client:
        db.drop_all()
        db.create_all()
        yield client

def test_register(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None

def test_login(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None

    resp = client.post('/login', json = {"email":"a@gmail.com", "password":"c"})
    assert resp.status_code == 200
    assert resp.data is not None

def test_profile(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    resp2 = client.get('/profile', headers = {"Authorization": "Bearer " + token})
    assert resp2.status_code == 200
    assert resp2.data is not None
