from app import models
import pytest
from app.database import get_db, Base
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.oath2 import create_access_token

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:13012004@localhost:5432/fastapi_test"

# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}' \
#                          f':{settings.database_password}@{settings.database_hostname}' \
#                          f':{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "dimasik4@gmail.com", "password": "12345", "name": "Dimasik"}
    res = client.post("users/new", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    new_user['email'] = user_data['email']

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {token}'
    }

    return client


@pytest.fixture
def test_posts(test_user, session):
    post_data = [{
        "title": "1 post",
        "content": "1 post c.",
        "owner_id": test_user['id']
    }, {
        "title": "2 post",
        "content": "2 post c.",
        "owner_id": test_user['id']
    }, {
        "title": "3 post",
        "content": "3 post c.",
        "owner_id": test_user['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    posts_l = list(post_map)

    session.add_all(posts_l)
    session.commit()

    posts = session.query(models.Post).all()

    return posts
