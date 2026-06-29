# app/clients/http.py
import httpx
from typing import Optional

_client: Optional[httpx.AsyncClient] = None


def get_client() -> httpx.AsyncClient:
    """Получить глобальный клиент. Вызывать только после startup."""
    if _client is None:
        raise RuntimeError("HTTP client not initialized")
    return _client


async def init_client():
    global _client
    _client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0, connect=5.0),
        follow_redirects=False,   # важно! редиректы отслеживаем вручную
        limits=httpx.Limits(max_connections=20),
        headers={"User-Agent": "Mozilla/5.0 (SiteAuditBot/1.0)"}
    )


async def close_client():
    global _client
    if _client:
        await _client.aclose()
        _client = None