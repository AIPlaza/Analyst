import httpx
from datetime import datetime

BASE_URL = "https://api.coingecko.com/api/v3"

async def ping():
    """Check API status."""
    url = f"{BASE_URL}/ping"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

async def get_oxt_market_chart(vs_currency: str = "usd", days: str = "max"):
    """Get historical market data for OXT (price, market cap, and 24h volume)."""
    url = f"{BASE_URL}/coins/orchid/market_chart"
    params = {"vs_currency": vs_currency, "days": days}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
