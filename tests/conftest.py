import pytest
from unittest.mock import patch
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from typing import Generator
from httpx import AsyncClient
from asyncio import get_event_loop
from app.ext.db import engine
from app.main import app

@pytest.fixture
async def async_client() -> Generator:

    fake_sqlite = 'sqlite:///database_fake.db'
    with patch('app.ext.db.db_url', new=fake_sqlite):
        SQLModel.metadata.drop_all(bind=engine)
        SQLModel.metadata.create_all(bind=engine)

        async with AsyncClient(app=app, base_url= "http://localhost:8000") as client:
            yield client


@pytest.fixture(scope="module")
def event_loop():

    loop = get_event_loop()
    yield loop
