import asyncio
import os
from typing import AsyncIterator, Generator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from fastapi import FastAPI

from app.config import Settings, settings

settings_override: Settings = Settings(
    database_url=os.environ.get("DATABASE_TEST_URL"),
    secret_key="suddenpillow",
    algorithm="HS256",
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncIterator[FastAPI]:
    import app.main

    yield app.main.app


@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI) -> AsyncIterator[TestClient]:
    app.dependency_overrides[settings] = settings_override
    async with TestClient(app) as client:
        yield client
