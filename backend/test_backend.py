import pytest
import json
from server import app, db
from pathlib import Path
from datetime import datetime

content = Path(__file__).parent / "content"

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

def test_register_password_mismatch(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "d"})
    assert resp.status_code == 400
    assert resp.data == b'"Passwords do not match"\n'

def test_register_empty_email(client):

    resp = client.post('/register', json = {"email":"", "name":"b", "password":"c", "passwordconfirmation": "d"})
    assert resp.status_code == 400
    assert resp.data == b'"Empty Email"\n'

def test_register_empty_name(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"", "password":"c", "passwordconfirmation": "d"})
    assert resp.status_code == 400
    assert resp.data == b'"Empty Name"\n'

def test_register_empty_password(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"", "passwordconfirmation": "d"})
    assert resp.status_code == 400
    assert resp.data == b'"Empty Password"\n'

def test_login(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None

    resp = client.post('/login', json = {"email":"a@gmail.com", "password":"c"})
    assert resp.status_code == 200
    assert resp.data is not None

def test_login_incorrect(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None

    resp = client.post('/login', json = {"email":"b@gmail.com", "password":"c"})
    assert resp.status_code == 401
    assert resp.data == b'Email or Password Incorrect'

def test_get_profile(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    resp2 = client.get('/profile', headers = {"Authorization": "Bearer " + token})
    assert resp2.status_code == 200
    assert resp2.data is not None
    data = json.loads(resp2.data.decode('utf8').strip())
    assert data['email'] == "a@gmail.com"
    assert data['default_days'] == 3

def test_get_missing_profile(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    db.drop_all()
    db.create_all()

    resp2 = client.get('/profile', headers = {"Authorization": "Bearer " + token})
    assert resp2.status_code == 404
    assert resp2.data == b'User not found'

def test_post_profile(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    resp2 = client.post('/profile', json = {"password":"", "newpassword":"", "newpasswordconfirmation":"", "defaultdays":3},headers = {"Authorization": "Bearer " + token})
    assert resp2.data == b'"Nothing new"\n'
    assert resp2.status_code == 200

def test_post_profile_change_password(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    resp2 = client.post('/profile', json = {"password":"c", "newpassword":"d", "newpasswordconfirmation":"d", "defaultdays":3},headers = {"Authorization": "Bearer " + token})
    assert resp2.data == b'"Password changed"\n'
    assert resp2.status_code == 200

    resp = client.post('/login', json = {"email":"a@gmail.com", "password":"d"})
    assert resp.status_code == 200
    assert resp.data is not None

def test_post_profile_change_password_orignal_password_incorrect(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    resp2 = client.post('/profile', json = {"password":"e", "newpassword":"d", "newpasswordconfirmation":"d", "defaultdays":3},headers = {"Authorization": "Bearer " + token})
    assert resp2.data == b'Passwords do not match'
    assert resp2.status_code == 401


def test_post_profile_change_password_new_password_mismatch(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    resp2 = client.post('/profile', json = {"password":"c", "newpassword":"d", "newpasswordconfirmation":"e", "defaultdays":3},headers = {"Authorization": "Bearer " + token})
    assert resp2.data == b'new password does not match'
    assert resp2.status_code == 400

def test_post_profile_change_notification_day(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    resp2 = client.post('/profile', json = {"password":"c", "newpassword":"", "newpasswordconfirmation":"", "defaultdays":4},headers = {"Authorization": "Bearer " + token})
    assert resp2.data == b'"Default notification day changed"\n'
    assert resp2.status_code == 200

    resp2 = client.get('/profile', headers = {"Authorization": "Bearer " + token})
    assert resp2.status_code == 200
    assert resp2.data is not None
    data = json.loads(resp2.data.decode('utf8').strip())
    assert data['email'] == "a@gmail.com"
    assert data['default_days'] == 4

def test_post_profile_change_notification_day_change_password(client):

    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    resp2 = client.post('/profile', json = {"password":"c", "newpassword":"d", "newpasswordconfirmation":"d", "defaultdays":4},headers = {"Authorization": "Bearer " + token})
    assert resp2.data == b'"Password changed and default notification day changed"\n'
    assert resp2.status_code == 200

    resp2 = client.get('/profile', headers = {"Authorization": "Bearer " + token})
    assert resp2.status_code == 200
    assert resp2.data is not None
    data = json.loads(resp2.data.decode('utf8').strip())
    assert data['email'] == "a@gmail.com"
    assert data['default_days'] == 4

    resp = client.post('/login', json = {"email":"a@gmail.com", "password":"d"})
    assert resp.status_code == 200
    assert resp.data is not None

def test_logout(client):
    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    resp2 = client.post('/logout', headers = {"Authorization": "Bearer " + token})
    assert resp2.status_code == 200
    assert resp2.data == b'You have been logged out'

    resp2 = client.get('/profile', headers = {"Authorization": "Bearer " + token})
    assert resp2.status_code == 401
    assert resp2.data == b'This user is logged out'


def test_prediction(client):
    resp = client.post('/register', json = {"email":"a@gmail.com", "name":"b", "password":"c", "passwordconfirmation": "c"})
    assert resp.status_code == 201
    assert resp.data is not None
    token = json.loads(resp.data.decode('utf8').strip())["access_token"]

    resp = client.post('/prediction',data={"fruittype":"Apple", "latitude":"33.8688", "longitude":"151.2093","purchaseDate":"2024-11-6", "file": (content / "apple-day.jpg").open("rb")} ,headers = {"Authorization": "Bearer " + token})
    assert resp.status_code == 200
    assert b'Expiry is 3 days from now, which is' in resp.data
