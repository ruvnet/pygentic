import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_create_assistant():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/v1/assistants",
            json={"id": "1", "name": "Test Assistant", "model": "gpt-4"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Test Assistant"
