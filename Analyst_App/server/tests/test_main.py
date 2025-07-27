import sys
import os
from fastapi.testclient import TestClient

# Add the parent directory (Analyst_App/server) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

# This test requires a running CoinGecko API and might be flaky
# def test_ping_coingecko():
#     response = client.get("/ping")
#     assert response.status_code == 200
#     assert "gecko_says" in response.json()