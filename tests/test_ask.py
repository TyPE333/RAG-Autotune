from app.main import app
from httpx import AsyncClient, ASGITransport
import pytest


payload = {
    "question": "What is the capital of France?"
}

@pytest.mark.asyncio
async def test_ask_endpoint():
    """
    should POST a sample question and assert the JSON contains "answer".
    """
    transport = ASGITransport(app=app)  # Create transport
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/ask", json = payload)

    assert res.status_code == 200

    json_data = res.json()
    print(json_data)  # Check the error details


    assert "answer" in json_data
