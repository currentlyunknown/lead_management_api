from async_asgi_testclient import TestClient
from fastapi import status
import pytest

BASE_URL = "/"


@pytest.mark.asyncio
async def test_api_is_running(client: TestClient) -> None:
    response = await client.get(BASE_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "The server is running"
