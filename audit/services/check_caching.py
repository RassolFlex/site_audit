"""Проверка заголовков кэширования."""
import requests
from datetime import datetime, timezone


def check_caching(url):
    """Проверка заголовков кэширования.

    Args:
        url: URL страницы

    Returns:
        dict с Cache-Control, Expires, Last-Modified и статусом конфигурации кэширования
    """
    result = {
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "source": "Python requests",
        "cache_control": None,
        "expires": None,
        "last_modified": None,
        "etag": None,
        "caching_configured": None,
        "error": None
    }

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=10, headers=headers)
        
        result['cache_control'] = response.headers.get('Cache-Control') or ''
        result['expires'] = response.headers.get('Expires') or None
        result['last_modified'] = response.headers.get('Last-Modified') or None
        result['etag'] = response.headers.get('ETag') or None
        
        # Определение, настроено ли кэширование
        cc = result['cache_control'] or ''
        
        has_public = 'public' in cc.lower() if cc else False
        has_max_age = bool(re.search(r'\bmax-age\s*=\s*\d+', cc)) if cc else False
        
        import re
        
        result['caching_configured'] = has_public or has_max_age or bool(result['expires']) or bool(result['etag'])
        
    except Exception as e:
        result['error'] = f"Ошибка проверки кэширования: {str(e)}"
    
    return result


__all__ = ["check_caching"]