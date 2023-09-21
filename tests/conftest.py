import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from httpx import AsyncClient

from main import app
from src.db.main import get_db, Base
from settings import settings

engine = create_async_engine(settings.db_dsn_test)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        pass

app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def connect_then_flus_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
def api_client() -> AsyncClient:
    return AsyncClient(app=app, base_url="http://0.0.0.0:8099")


@pytest.fixture(scope="function")
def get_session():
    return SessionLocal

@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_user_data():
    return {"name": "Test", "phone": "79996663322", 
            "email": "test@test.test", "password": "test_password_123"}