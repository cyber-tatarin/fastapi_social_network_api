import pytest

from app import schemas
from jose import jwt
from app.config import settings


def test_create_user(client):
    res = client.post("/users/new", json={'email': 'dimasik888@gmail.com', 'password': '12345', 'name': 'Dimasik'})

    new_user = schemas.RespUser(**res.json())

    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    id = str(payload.get("user_id"))

    assert id == test_user['id']
    assert res.status_code == 200
    assert login_res.token_type == 'bearer'


@pytest.mark.parametrize('email, password, status_code', [
    ('1', '2', 403),
    ('dimasik4@gmail.com', '2', 403),
    ('1', '12345', 403),
    (None, '12345', 422),
    ('dimasik4@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
#    assert res.json().get('detail') == "Invalid credentials"

