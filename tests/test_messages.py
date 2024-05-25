import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_add_message():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/v1/threads/1/messages",
            json={"id": "1", "thread_id": "1", "role": "user", "content": "Hello"},
        )
        assert response.status_code == 200
        assert response.json()["content"] == "Hello"
