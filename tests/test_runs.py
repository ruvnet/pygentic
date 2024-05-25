import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_run_thread():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/v1/threads/1/runs",
            json={
                "id": "1",
                "thread_id": "1",
                "assistant_id": "1",
                "status": "running",
            },
        )
        assert response.status_code == 200
        assert response.json()["status"] == "running"
