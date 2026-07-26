from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app

database_url = settings.database_url+"_test"

engine = create_engine(database_url)

TestingSessionLocal = sessionmaker(
    bind=engine, 
    autocommit= False,
    autoflush= False
)

@pytest.fixture(scope="function")
def session():
    print("session fixture run")
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