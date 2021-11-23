import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy_utils import drop_database
from sqlmodel.pool import StaticPool
from typing import Generator
from app.main import app
from app.ext.core.utils import get_session


@pytest.fixture(name="session")
def session_fixture():

    engine = create_engine(
        'sqlite:///database_fake.db',
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    drop_database('sqlite:///database_fake.db')


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
