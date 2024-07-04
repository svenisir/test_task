import asyncio

import pytest
from fastapi.testclient import TestClient  # noqa
from httpx import AsyncClient

from app.main import app as fastapi_app
from app.database import Base, async_session_maker, engine
from app.config import settings
from app.memes.model import Memes  # noqa
from app.users.model import Users  # noqa


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(url="/auth/register", json={
            "email": "test@test.com",
            "password": "test"
        })

        await ac.post(url="/auth/login", json={
            "email": "test@test.com",
            "password": "test"
        })

        assert ac.cookies["booking_access_token"]
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session



