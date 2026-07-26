from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.security import create_access_token
from app.core.database import Base, get_db
from app.models.posts import Post
from app.main import app

database_url = settings.database_url

engine = create_engine(database_url)

TestingSessionLocal = sessionmaker(
    bind=engine, 
    autocommit= False,
    autoflush= False
)

@pytest.fixture(scope="function")
def session():
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
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

    user_data = {
        "username": "arian",
        "email": "arian@gmail.com",
        "password": "arian12345"
    }

    res = client.post(
        "/resister",
        data=user_data
    )

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["userid"]})

@pytest.fixture 
def authorized_client(client, token):
    client.headers = {
        **client.headers, 
        "Authorization" : f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_user2(client):

    user_data = {
        "username": "arian2",
        "email": "arian2@gmail.com",
        "password": "arian123452"
    }

    res = client.post(
        "/resister",
        data=user_data
    )

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user

@pytest.fixture
def test_posts(test_user, session, test_user2):

    posts_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "user_id": test_user["userid"]
        }, {
            "title": "2nd title",
            "content": "2nd content",
            "user_id": test_user["userid"]
        }, {
            "title": "3rd title",
            "content": "3rd content",
            "user_id": test_user["userid"]
        },{
            "title": "4th title",
            "content": "4th content",
            "user_id": test_user2["userid"]
        }
    ]

    def create_post_model(post):
        return Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(Post).all()
    return posts