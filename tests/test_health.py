from app.main import app
from httpx import AsyncClient, ASGITransport
import pytest

@pytest.mark.asyncio
async def test_health_endpoint_status_code_200():
    transport = ASGITransport(app=app)  # Create transport
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/health")
    assert res.status_code == 200
