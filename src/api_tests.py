import pytest
from database import init_test_db
from httpx import AsyncClient, ASGITransport    
from main import app

schema_URL = {"long_url":"https://example.com/"}



@pytest.mark.asyncio
async def test_post_url():
    await init_test_db()

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        response = await ac.post("/posturl", json=schema_URL)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_redirect():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        response = await ac.get("/0f115")
        assert response.status_code == 307
